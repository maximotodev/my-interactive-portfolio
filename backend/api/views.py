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
# from sklearn.feature_extraction.text import TfidfVectorizer
from django.db.models import Q # Add Q object for complex lookups
import re # Add regex module for splitting query
# from sklearn.metrics.pairwise import cosine_similarity
# from sentence_transformers import SentenceTransformer

# --- FINAL, CORRECT NOSTR LIBRARY BASED ON DOCUMENTATION ---
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
# --- NEW: Choose a lightweight but effective sentence transformer model ---
# SENTENCE_MODEL_NAME = 'all-MiniLM-L6-v2'
# ==============================================================================
# Global Model Cache (for performance)
# ==============================================================================

# This dictionary will act as a simple in-memory cache for our AI model.
# This prevents reloading the ~80MB model from disk on every single API call.
# model_cache = {}

# def get_sentence_transformer_model():
#     """
#     Loads the Sentence Transformer model from cache or from disk if not loaded.
#     """
#     if SENTENCE_MODEL_NAME not in model_cache:
#         print(f"Loading sentence transformer model: {SENTENCE_MODEL_NAME}...")
#         model_cache[SENTENCE_MODEL_NAME] = SentenceTransformer(SENTENCE_MODEL_NAME)
#         print("Model loaded successfully.")
#     return model_cache[SENTENCE_MODEL_NAME]
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
    # This function is now stable and correct
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
        while relay_manager.message_pool.has_events():
            event_msg = relay_manager.message_pool.get_event()
            # Find the latest event in case multiple relays respond
            if profile_data is None or event_msg.event.created_at > profile_data.get('created_at', 0):
                current_profile = json.loads(event_msg.event.content)
                current_profile['created_at'] = event_msg.event.created_at
                profile_data = current_profile
    finally:
        relay_manager.close_all_relay_connections()

    if profile_data and 'created_at' in profile_data:
        del profile_data['created_at']
    return profile_data

# --- NEW FUNCTION TO FETCH LATEST NOTE ---
def fetch_latest_nostr_note():
    """
    Fetches the latest text note (kind 1) from Nostr relays.
    """
    npub = os.getenv('NOSTR_NPUB')
    if not npub: return None
    hex_pubkey = decode_npub(npub)
    if not hex_pubkey: return None

    relay_manager = RelayManager(timeout=4)
    for relay in NOSTR_RELAYS:
        relay_manager.add_relay(relay)

    # Filter for kind 1 (text note), limit 1 (the latest)
    filters = FiltersList([Filters(authors=[hex_pubkey], kinds=[EventKind.TEXT_NOTE], limit=1)])
    subscription_id = "latest_note_sub"
    relay_manager.add_subscription_on_all_relays(subscription_id, filters)

    latest_note = None
    try:
        relay_manager.run_sync()
        # The first event we get will be the latest one due to limit=1
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

# ... (all other fetch functions like github_stats, etc., remain the same)
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
    """
    API endpoint for published blog posts.
    Allows fetching a list of posts and a single post by its slug.
    """
    queryset = Post.objects.filter(is_published=True) # Only show published posts
    serializer_class = PostSerializer
    lookup_field = 'slug' # Use the slug for retrieving a single post
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
    contribution_cache_timeout = 21600 # 6 hours
    cached_data = cache.get(cache_key)
    if cached_data: return Response(cached_data)
    contribution_data = fetch_github_contributions_data()
    if contribution_data:
        cache.set(cache_key, contribution_data, timeout=contribution_cache_timeout)
        return Response(contribution_data)
    return Response({'error': 'Failed to fetch contribution data.'}, status=502)

# --- NEW VIEW FOR THE LATEST NOTE ---
@api_view(['GET'])
def latest_note(request):
    """
    Provides my latest Nostr note (kind 1), cached for 15 minutes.
    """
    npub = os.getenv('NOSTR_NPUB')
    if not npub: return Response({'error': 'Nostr npub not configured.'}, status=500)

    cache_key = f"latest_note_{npub}"
    cached_data = cache.get(cache_key)
    if cached_data: return Response(cached_data)
        
    note_data = fetch_latest_nostr_note()
    if note_data:
        cache.set(cache_key, note_data, timeout=900) # Cache for 15 minutes
        return Response(note_data)
    
    return Response({'error': 'No recent note found.'}, status=404)

# --- REFACTORED AI/ML SKILL MATCHER VIEW ---
# @api_view(['POST'])
# def skill_match_view(request):
#     """
#     AI Skill Matcher is temporarily disabled for deployment on the free tier
#     due to memory constraints. It returns an empty list to prevent errors.
#     """
#     print("INFO: AI Skill Matcher endpoint called, returning empty list (feature disabled).")
#     # By returning an empty list, the frontend will correctly show "No projects match your query."
#     return Response([])
    # """
    # Uses a HYBRID approach.
    # 1. Filters projects by keyword in the 'technologies' field.
    # 2. Ranks the results semantically. Guarantees that keyword matches appear.
    # 3. Falls back to full semantic search if no keywords match.
    # """
    # SIMILARITY_THRESHOLD = 0.30  # Threshold for the fallback semantic search

    # query = request.data.get('query', '').strip()
    # if not query:
    #     return Response([])

    # keywords = [word for word in re.split(r'[,\s]+', query) if word]
    
    # keyword_query = Q()
    # for keyword in keywords:
    #     keyword_query |= Q(technologies__icontains=keyword) | Q(description__icontains=keyword) | Q(title__icontains=keyword)
    
    # keyword_matched_projects = Project.objects.filter(keyword_query).distinct()

    # projects_to_process = []
    # is_keyword_search = False

    # if keyword_matched_projects.exists():
    #     print(f"[DEBUG] Found {keyword_matched_projects.count()} projects via keyword match.")
    #     projects_to_process = keyword_matched_projects
    #     is_keyword_search = True
    # else:
    #     print("[DEBUG] No keyword match. Falling back to full semantic search.")
    #     projects_to_process = Project.objects.all()

    # if not projects_to_process:
    #     return Response([])

    # project_docs = [f"{p.title}. {p.description}. Technologies used: {p.technologies}" for p in projects_to_process]
    # project_ids = [p.id for p in projects_to_process]

    # try:
    #     model = get_sentence_transformer_model()
    #     project_embeddings = model.encode(project_docs)
    #     query_embedding = model.encode(query)

    #     cosine_scores = cosine_similarity([query_embedding], project_embeddings).flatten()

    #     matched_projects = []
    #     for i, score in enumerate(cosine_scores):
    #         # --- NEW LOGIC ---
    #         # If this was a keyword search, we include all results regardless of score,
    #         # as they are explicitly relevant.
    #         # If it was a fallback semantic search, we apply the threshold.
    #         if is_keyword_search or score >= SIMILARITY_THRESHOLD:
    #             matched_projects.append({'id': project_ids[i], 'score': float(score)})
        
    #     ranked_matches = sorted(matched_projects, key=lambda p: p['score'], reverse=True)
        
    #     return Response(ranked_matches)
        
    # except Exception as e:
    #     print(f"Error during hybrid skill matching: {e}")
    #     return Response({'error': 'An error occurred during skill analysis.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)