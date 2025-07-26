# backend/api/views.py

import os
import json
import time
from datetime import datetime, timedelta

# Django & DRF Imports
from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# External Libraries
import requests
from pynostr.relay_manager import RelayManager
from pynostr.filters import FiltersList, Filters
from pynostr.event import EventKind
from pynostr.key import PublicKey
from bitcoinlib.wallets import Wallet, WalletError

# Local Imports
from .models import Project, Certification, Post
from .serializers import ProjectSerializer, CertificationSerializer, PostSerializer

# --- Configuration Constants ---
GITHUB_USERNAME = "maximotodev"
NOSTR_RELAYS = ["wss://relay.damus.io", "wss://relay.primal.net", "wss://nos.lol", "wss://relay.nostr.band"]
CACHE_TIMEOUT_SECONDS = 3600  # 1 hour
BITCOIN_WALLET_NAME = "MyPortfolioWallet"

# ==============================================================================
# HELPER & SERVICE FUNCTIONS
# ==============================================================================

def decode_npub(npub: str) -> str | None:
    """Decodes an 'npub' to hex using pynostr's PublicKey class."""
    try:
        public_key = PublicKey.from_npub(npub)
        return public_key.hex()
    except Exception:
        return None

def fetch_nostr_profile_data():
    """Fetches the latest profile (kind 0) from Nostr relays."""
    npub = os.getenv('NOSTR_NPUB')
    if not npub: return None
    hex_pubkey = decode_npub(npub)
    if not hex_pubkey: return None

    relay_manager = RelayManager(timeout=6)
    for relay in NOSTR_RELAYS:
        relay_manager.add_relay(relay)
    
    filters = FiltersList([Filters(authors=[hex_pubkey], kinds=[EventKind.SET_METADATA], limit=1)])
    subscription_id = "profile_sub"
    relay_manager.add_subscription_on_all_relays(subscription_id, filters)
    
    profile_data = None
    try:
        relay_manager.run_sync()
        latest_event = None
        while relay_manager.message_pool.has_events():
            event_msg = relay_manager.message_pool.get_event()
            if latest_event is None or event_msg.event.created_at > latest_event.created_at:
                latest_event = event_msg.event
        if latest_event:
            profile_data = json.loads(latest_event.content)
    finally:
        relay_manager.close_all_relay_connections()
    return profile_data

def fetch_latest_nostr_note():
    """Fetches the latest text note (kind 1) from Nostr relays."""
    npub = os.getenv('NOSTR_NPUB')
    if not npub: return None
    hex_pubkey = decode_npub(npub)
    if not hex_pubkey: return None

    relay_manager = RelayManager(timeout=4)
    for relay in NOSTR_RELAYS:
        relay_manager.add_relay(relay)

    filters = FiltersList([Filters(authors=[hex_pubkey], kinds=[EventKind.TEXT_NOTE], limit=1)])
    subscription_id = "latest_note_sub"
    relay_manager.add_subscription_on_all_relays(subscription_id, filters)

    latest_note = None
    try:
        relay_manager.run_sync()
        if relay_manager.message_pool.has_events():
            event_msg = relay_manager.message_pool.get_event()
            latest_note = {
                "id": event_msg.event.id,
                "content": event_msg.event.content,
                "created_at": event_msg.event.created_at,
            }
    finally:
        relay_manager.close_all_relay_connections()
    return latest_note

def fetch_github_stats_data():
    """Fetches user stats from the GitHub REST API."""
    token = os.getenv('GITHUB_API_TOKEN')
    headers = {'Authorization': f'token {token}'} if token else {}
    try:
        user_url = f'https://api.github.com/users/{GITHUB_USERNAME}'
        user_response = requests.get(user_url, headers=headers, timeout=10)
        user_response.raise_for_status()
        user_data = user_response.json()
        repos_url = user_data['repos_url']
        repos_response = requests.get(repos_url, headers=headers, timeout=10)
        repos_response.raise_for_status()
        repos_data = repos_response.json()
        total_stars = sum(repo['stargazers_count'] for repo in repos_data)
        return { 'followers': user_data.get('followers'), 'public_repos': user_data.get('public_repos'), 'total_stars': total_stars }
    except requests.RequestException: return None

def fetch_github_contributions_data():
    """Fetches contribution calendar data from the GitHub GraphQL API."""
    token = os.getenv('GITHUB_API_TOKEN')
    if not token: return None
    headers = {"Authorization": f"bearer {token}"}
    graphql_endpoint = "https://api.github.com/graphql"
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=365)
    query = """
    query($userName: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $userName) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar { totalContributions weeks { contributionDays { contributionCount date weekday color } } }
        }
      }
    }
    """
    variables = { "userName": GITHUB_USERNAME, "from": start_date.isoformat() + "Z", "to": end_date.isoformat() + "Z" }
    try:
        response = requests.post(graphql_endpoint, json={'query': query, 'variables': variables}, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        if "errors" in data: return None
        return data['data']['user']['contributionsCollection']['contributionCalendar']
    except requests.RequestException: return None

def fetch_onchain_bitcoin_address():
    """
    Loads a persistent, deterministic Bitcoin wallet from a mnemonic
    stored in an environment variable.
    """
    wallet_name = "MyPortfolioWallet_prod" # Use a new name
    mnemonic = os.getenv('BITCOIN_WALLET_MNEMONIC')

    if not mnemonic:
        # This should never happen in production if the secret is set
        print("ERROR: BITCOIN_WALLET_MNEMONIC environment variable not set.")
        return None

    try:
        # This will load the wallet if it exists on the ephemeral disk.
        w = Wallet(wallet_name)
    except WalletError:
        # If it doesn't exist (e.g., after a deploy), CREATE it deterministically
        # from your permanent mnemonic seed phrase.
        print(f"INFO: Creating new DETERMINISTIC Bitcoin wallet from mnemonic: {wallet_name}")
        w = Wallet.create(wallet_name, keys=mnemonic, witness_type='segwit')
    
    # Get the first available key's address. This will be the same address every time.
    key = w.get_key()
    return {'address': key.address}

def fetch_mempool_data():
    """
    Fetches recommended fee rates, block height, hashrate, and BTC price.
    """
    mempool_base_url = "https://mempool.space/api"
    
    try:
        # Fetch all data points in parallel
        fees_response = requests.get(f"{mempool_base_url}/v1/fees/recommended", timeout=10)
        height_response = requests.get(f"{mempool_base_url}/blocks/tip/height", timeout=10)
        # Using the /v1/mining/hashrate endpoint is a good alternative
        hashrate_response = requests.get(f"{mempool_base_url}/v1/mining/hashrate/1d", timeout=10)
        # The correct price endpoint from mempool.space
        price_response = requests.get(f"{mempool_base_url}/v1/prices", timeout=10)

        # Check all responses for errors
        fees_response.raise_for_status()
        height_response.raise_for_status()
        hashrate_response.raise_for_status()
        price_response.raise_for_status()
        
        # Combine all the data into a single object
        return {
            "recommended_fees": fees_response.json(),
            "block_height": height_response.json(),
            "hashrate": hashrate_response.json().get('currentHashrate'),
            # --- THIS IS THE CORRECTED LINE ---
            # The key for the USD price in this endpoint is 'USD'
            "price": price_response.json().get('USD'),
        }
    except requests.RequestException as e:
        print(f"Error fetching mempool/price data: {e}")
        return None
# ==============================================================================
# API VIEWS
# ==============================================================================
class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all().order_by('-id')
    serializer_class = ProjectSerializer

class CertificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Certification.objects.all().order_by('-date_issued')
    serializer_class = CertificationSerializer

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer
    lookup_field = 'slug'

@api_view(['GET'])
def bitcoin_address(request):
    cache_key = f"bitcoin_address_{BITCOIN_WALLET_NAME}"
    cached_data = cache.get(cache_key)
    if cached_data: return Response(cached_data)
    address_data = fetch_onchain_bitcoin_address()
    if address_data:
        cache.set(cache_key, address_data, timeout=None)
        return Response(address_data)
    return Response({'error': 'Failed to generate Bitcoin address.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def nostr_profile(request):
    npub = os.getenv('NOSTR_NPUB')
    if not npub: return Response({'error': 'Nostr npub not configured.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    cache_key = f"nostr_profile_{npub}"
    cached_data = cache.get(cache_key)
    if cached_data: return Response(cached_data)
    profile_data = fetch_nostr_profile_data()
    if profile_data:
        profile_data['npub'] = npub
        cache.set(cache_key, profile_data, timeout=CACHE_TIMEOUT_SECONDS)
        return Response(profile_data)
    return Response({'error': 'Nostr profile not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def latest_note(request):
    npub = os.getenv('NOSTR_NPUB')
    if not npub: return Response({'error': 'Nostr npub not configured.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    cache_key = f"latest_note_{npub}"
    cached_data = cache.get(cache_key)
    if cached_data: return Response(cached_data)
    note_data = fetch_latest_nostr_note()
    if note_data:
        cache.set(cache_key, note_data, timeout=900) # 15 minutes
        return Response(note_data)
    return Response({'error': 'No recent note found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def github_stats(request):
    cache_key = f"github_stats_{GITHUB_USERNAME}"
    cached_data = cache.get(cache_key)
    if cached_data: return Response(cached_data)
    stats_data = fetch_github_stats_data()
    if stats_data:
        cache.set(cache_key, stats_data, timeout=CACHE_TIMEOUT_SECONDS)
        return Response(stats_data)
    return Response({'error': 'Failed to fetch from GitHub.'}, status=status.HTTP_502_BAD_GATEWAY)

@api_view(['GET'])
def github_contributions(request):
    cache_key = f"github_contributions_{GITHUB_USERNAME}"
    contribution_cache_timeout = 21600 # 6 hours
    cached_data = cache.get(cache_key)
    if cached_data: return Response(cached_data)
    contribution_data = fetch_github_contributions_data()
    if contribution_data:
        cache.set(cache_key, contribution_data, timeout=contribution_cache_timeout)
        return Response(contribution_data)
    return Response({'error': 'Failed to fetch contribution data.'}, status=status.HTTP_502_BAD_GATEWAY)

@api_view(['GET'])
def mempool_stats(request):
    """Provides live Bitcoin mempool stats, cached for 60 seconds."""
    cache_key = "mempool_stats"
    mempool_cache_timeout = 60
    cached_data = cache.get(cache_key)
    if cached_data:
        return Response(cached_data)
    data = fetch_mempool_data()
    if data:
        cache.set(cache_key, data, timeout=mempool_cache_timeout)
        return Response(data)
    return Response({'error': 'Failed to fetch data from mempool.space API.'}, status=status.HTTP_502_BAD_GATEWAY)