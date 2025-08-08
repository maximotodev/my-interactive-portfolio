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
from django.http import StreamingHttpResponse
from .ai_service import KnowledgeBaseService 
from .ai_prompts import JSON_SYSTEM_PROMPT, CONVERSATIONAL_SYSTEM_PROMPT
from .llm_streaming import stream_llm_response # <- We'll move the LLM logic here
# External Libraries
import requests
from pynostr.relay_manager import RelayManager
from pynostr.filters import FiltersList, Filters
from pynostr.event import EventKind
from pynostr.key import PublicKey
from bitcoinlib.wallets import Wallet, WalletError
from groq import Groq

# Local Imports
# --- IMPORT ALL YOUR MODELS ---
from .models import Project, Certification, Post, WorkExperience
from .serializers import ProjectSerializer, CertificationSerializer, PostSerializer, WorkExperienceSerializer

# --- Configuration Constants ---
GITHUB_USERNAME = "maximotodev"
NOSTR_RELAYS = ["wss://relay.damus.io", "wss://relay.primal.net", "wss://nos.lol", "wss://relay.nostr.band"]
CACHE_TIMEOUT_SECONDS = 3600  # 1 hour
BITCOIN_WALLET_NAME = "MyPortfolioWallet"
HUGGINGFACE_EMBEDDING_MODEL_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"

# ==============================================================================
# HELPER & SERVICE FUNCTIONS # ==============================================================================

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
            "price": price_response.json().get('USD'),
        }
    except requests.RequestException as e:
        print(f"Error fetching mempool/price data: {e}")
        return None

# ==============================================================================
# API VIEWS
# ==============================================================================

class WorkExperienceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer

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

@api_view(['POST'])
def skill_match_view(request):
    """
    Uses the Hugging Face Inference API for semantic search.
    This is safe to run on a free-tier server.
    """
    query = request.data.get('query', '')
    if not query.strip():
        return Response([])

    projects = Project.objects.all()
    if not projects.exists():
        return Response([])

    project_docs = [f"{p.title}. {p.description}. Technologies: {p.technologies}" for p in projects]
    project_ids = [p.id for p in projects]
    
    try:
        token = os.getenv('HUGGINGFACE_API_TOKEN')
        if not token:
            raise ValueError("Hugging Face API token is not set.")
            
        headers = {"Authorization": f"Bearer {token}"}
        
        payload = {
            "inputs": {
                "source_sentence": query,
                "sentences": project_docs
            }
        }
        
        response = requests.post(HUGGINGFACE_EMBEDDING_MODEL_URL, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        scores = response.json() 

        if not isinstance(scores, list):
            print(f"Unexpected response from Hugging Face API: {scores}")
            raise ValueError("Invalid response format from embedding API.")

        results = sorted(zip(project_ids, scores), key=lambda item: item[1], reverse=True)
        
        ranked_projects = [{'id': pid, 'score': float(score)} for pid, score in results if score > 0.3]
        return Response(ranked_projects)

    except Exception as e:
        print(f"Error calling Hugging Face API: {e}")
        keywords = query.lower().split()
        matched_ids = set()
        for p in projects:
            project_text = f"{p.title} {p.technologies}".lower()
            if any(keyword in project_text for keyword in keywords):
                matched_ids.add(p.id)
        
        fallback_projects = [{'id': pid, 'score': 1.0} for pid in matched_ids]
        return Response(fallback_projects)

# ==============================================================================
# AI CAREER CHAT - API VIEW (FINAL scikit-learn VERSION)
# ==============================================================================
@api_view(['POST'])
def career_chat(request):
    user_question = request.data.get('question', '').lower()
    if not user_question:
        return Response({'error': 'Question is required.'}, status=400)

    kb_service = KnowledgeBaseService()
    
    intents = {
        'project': ['project', 'projects', 'portfolio', 'show me his projects'],
        'experience': ['experience', 'resume', 'cv', 'history', 'work experience', 'summarize experience'],
        'certification': ['certification', 'certifications', 'credential', 'education', 'degree'],
        'blog': ['post', 'posts', 'blog', 'writing', 'article', 'blog writings'],
        'tech_stack': ['tech', 'stack', 'technologies', 'skill', 'skills', 'language', 'framework', 'frameworks']
    }
    
    detected_intent_type = None
    for intent_type, keywords in intents.items():
        if any(keyword in user_question for keyword in keywords):
            detected_intent_type = intent_type
            break

    if detected_intent_type:
        retrieved_docs = kb_service.get_all_by_type(detected_intent_type)
        system_prompt_to_use = JSON_SYSTEM_PROMPT
    else:
        retrieved_docs = kb_service.search(user_question)
        system_prompt_to_use = CONVERSATIONAL_SYSTEM_PROMPT

    context_str = "\n---\n".join([f"### DOCUMENT START\n{json.dumps(doc)}\n### DOCUMENT END" for doc in retrieved_docs])
    
    return StreamingHttpResponse(stream_llm_response(user_question, context_str, system_prompt_to_use), content_type="text/event-stream")