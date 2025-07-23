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
CACHE_TIMEOUT_SECONDS = 3600
BITCOIN_WALLET_NAME = "MyPortfolioWallet"

# ==============================================================================
# HELPER & SERVICE FUNCTIONS
# ==============================================================================

def decode_npub(npub: str) -> str | None:
    try:
        public_key = PublicKey.from_npub(npub)
        return public_key.hex()
    except Exception:
        return None

def fetch_nostr_profile_data():
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
            latest_note = {"id": event_msg.event.id, "content": event_msg.event.content, "created_at": event_msg.event.created_at}
    finally:
        relay_manager.close_all_relay_connections()
    return latest_note

def fetch_github_stats_data():
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
    try:
        w = Wallet(BITCOIN_WALLET_NAME)
    except WalletError:
        w = Wallet.create(BITCOIN_WALLET_NAME, witness_type='segwit')
    key = w.get_key()
    return {'address': key.address}

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
    return Response({'error': 'Failed to generate Bitcoin address.'}, status=500)
@api_view(['GET'])
def nostr_profile(request):
    npub = os.getenv('NOSTR_NPUB')
    if not npub: return Response({'error': 'Nostr npub not configured.'}, status=500)
    cache_key = f"nostr_profile_{npub}"
    cached_data = cache.get(cache_key)
    if cached_data: return Response(cached_data)
    profile_data = fetch_nostr_profile_data()
    if profile_data:
        cache.set(cache_key, profile_data, timeout=CACHE_TIMEOUT_SECONDS)
        return Response(profile_data)
    return Response({'error': 'Nostr profile not found.'}, status=404)
@api_view(['GET'])
def latest_note(request):
    npub = os.getenv('NOSTR_NPUB')
    if not npub: return Response({'error': 'Nostr npub not configured.'}, status=500)
    cache_key = f"latest_note_{npub}"
    cached_data = cache.get(cache_key)
    if cached_data: return Response(cached_data)
    note_data = fetch_latest_nostr_note()
    if note_data:
        cache.set(cache_key, note_data, timeout=900)
        return Response(note_data)
    return Response({'error': 'No recent note found.'}, status=404)
@api_view(['GET'])
def github_stats(request):
    cache_key = f"github_stats_{GITHUB_USERNAME}"
    cached_data = cache.get(cache_key)
    if cached_data: return Response(cached_data)
    stats_data = fetch_github_stats_data()
    if stats_data:
        cache.set(cache_key, stats_data, timeout=CACHE_TIMEOUT_SECONDS)
        return Response(stats_data)
    return Response({'error': 'Failed to fetch from GitHub.'}, status=502)
@api_view(['GET'])
def github_contributions(request):
    cache_key = f"github_contributions_{GITHUB_USERNAME}"
    cached_data = cache.get(cache_key)
    if cached_data: return Response(cached_data)
    contribution_data = fetch_github_contributions_data()
    if contribution_data:
        cache.set(cache_key, contribution_data, timeout=21600)
        return Response(contribution_data)
    return Response({'error': 'Failed to fetch contribution data.'}, status=502)

# The skill_match_view is no longer needed.