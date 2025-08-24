# backend/api/views.py
from django.http import StreamingHttpResponse
import os
import json
import time
from datetime import datetime, timedelta

# Django & DRF Imports
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
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
from groq import Groq

# Local Imports
# --- IMPORT ALL YOUR MODELS ---
from .models import Project, Certification, Post, WorkExperience, Tag
from .serializers import ProjectSerializer, CertificationSerializer, PostSerializer, WorkExperienceSerializer, TagSerializer

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
class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for listing all available tags.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class WorkExperienceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all().order_by('-id')

    # --- 2. ADD FILTERING LOGIC ---
    def get_queryset(self):
        """
        Optionally filter the projects by a 'tag' query parameter.
        """
        queryset = super().get_queryset()
        tag_slug = self.request.query_params.get('tag')
        if tag_slug:
            # Filter the queryset to only include projects that have a tag with the given slug
            queryset = queryset.filter(tags__slug=tag_slug)
        return queryset

class CertificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Certification.objects.all().order_by('-date_issued')
    serializer_class = CertificationSerializer

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(is_published=True)
    lookup_field = 'slug'

    # --- 3. ADD FILTERING LOGIC HERE TOO ---
    def get_queryset(self):
        """
        Optionally filter the posts by a 'tag' query parameter.
        """
        queryset = super().get_queryset()
        tag_slug = self.request.query_params.get('tag')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        return queryset
    
# --- NEW: NATIVE Full-Text Search API View ---
@api_view(['GET'])
def search_view(request):
    """
    Performs a full-text search across projects and posts using
    Django's native PostgreSQL integration.
    """
    query_param = request.GET.get('q', '')
    if not query_param:
        return Response({"error": "A 'q' query parameter is required."}, status=400)

    # Use SearchQuery to parse the user's input safely
    search_query = SearchQuery(query_param)

    # --- Search Projects ---
    # Create a SearchVector on the fly, combining the fields we want to search
    project_vector = SearchVector('title', 'description', 'tags__name', weight='A')
    
    # Annotate each project with a 'rank' based on how well it matches the query
    project_results = Project.objects.annotate(
        rank=SearchRank(project_vector, search_query)
    ).filter(rank__gte=0.1).order_by('pk', '-rank').distinct('pk')

    # --- Search Posts ---
    post_vector = SearchVector('title', 'content', 'tags__name', weight='B') # Give posts a slightly lower weight

    post_results = Post.objects.annotate(
        rank=SearchRank(post_vector, search_query)
    ).filter(is_published=True, rank__gte=0.1).order_by('pk', '-rank').distinct('pk')


    # Serialize the ranked results
    project_serializer = ProjectSerializer(project_results, many=True)
    post_serializer = PostSerializer(post_results, many=True)

    # Combine and return the final data
    return Response({
        'projects': project_serializer.data,
        'posts': post_serializer.data
    })
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
# AI CAREER CHAT - FINAL PRODUCTION VERSION
# ==============================================================================

def build_knowledge_base():
    """Builds the complete, topic-aware knowledge base with STANDARDIZED types."""
    # This function is already well-structured and remains the same.
    projects = Project.objects.all(); certifications = Certification.objects.all(); work_experiences = WorkExperience.objects.all(); posts = Post.objects.filter(is_published=True)
    knowledge_base_docs = []
    
    # Standardized type: "experience"
    for exp in work_experiences:
        responsibilities = [f'"{r.strip()}"' for r in exp.responsibilities.split('\n') if r.strip()]
        knowledge_base_docs.append(f"Type: experience. Title: \"{exp.job_title}\", Company: \"{exp.company_name}\", Date: \"{exp.start_date.strftime('%b %Y')} - {exp.end_date.strftime('%b %Y') if exp.end_date else 'Present'}\", Responsibilities: [{', '.join(responsibilities)}]")
    
    # Standardized type: "project"
    for p in projects:
        techs = [f'"{t.strip()}"' for t in p.technologies.split(',')]
        knowledge_base_docs.append(f"Type: project. Title: \"{p.title}\", Description: \"{p.description.replace('\"', '')}\", URL: \"{p.live_url}\", Repo_URL: \"{p.repository_url}\", Technologies: [{', '.join(techs)}]")
    
    # Standardized type: "certification"
    for c in certifications:
        knowledge_base_docs.append(f"Type: certification. Name: \"{c.name}\", Issuer: \"{c.issuing_organization}\", URL: \"{c.credential_url}\"")
    
    # Standardized type: "blog"
    frontend_url = os.getenv('FRONTEND_URL', 'https://maximotodev.vercel.app')
    for post in posts:
        knowledge_base_docs.append(f"Type: blog. Title: \"{post.title}\", URL: \"{frontend_url}/blog/{post.slug}\", Excerpt: \"{post.content[:200].replace('\"', '')}...\"")
    
    # Standardized type: "tech_stack"
    all_technologies = set()
    for project in projects:
        all_technologies.update([tech.strip() for tech in project.technologies.split(',') if tech.strip()])
    if all_technologies:
        knowledge_base_docs.append(f"Type: tech_stack. Technologies: [{', '.join([f'\"{tech}\"' for tech in sorted(list(all_technologies), key=str.lower)])}]")

    # Topic-Specific Context
    knowledge_base_docs.append("Type: topic. Name: Bitcoin. Details: Maximoto is a passionate Bitcoin maximalist with deep knowledge of its principles. This is demonstrated by his professional experience at Tribe BTC, a Bitcoin-focused company, and the inclusion of an on-chain Bitcoin tipping feature in his own portfolio project.")
    knowledge_base_docs.append("Type: topic. Name: Linux. Details: Maximoto holds a 'Linux and SQL' certification from Coursera, which validates his foundational skills in Linux environments and command-line operations.")
    knowledge_base_docs.append("Type: topic. Name: General Persona. Details: Maximoto's passion is in building beautiful, functional applications that leverage modern AI and decentralized technologies. He is a strong believer in open-source and continuous learning.")
    
    return knowledge_base_docs


# --- Modify the stream_llm_response function ---
def stream_llm_response(user_question, context, chat_history):
    try:
        client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        
        # --- NEW: Format the history for the LLM ---
        formatted_history = ""
        if chat_history:
            for message in chat_history:
                role = "User" if message['role'] == 'user' else "Assistant"
                formatted_history += f"{role}: {message['content']}\n"
        system_prompt = (
            "You are 'Maxi', an AI Chief of Staff. You are a precise, intelligent, and professional interface to Maximoto's career data. Your communication is flawless, and you follow instructions with 100% accuracy.\n\n"
            "**CORE DIRECTIVE: YOUR ONE AND ONLY TASK**\n"
            "Analyze the user's question and the provided context, then generate a single, clean response in one of two formats: 1. Structured JSON, 2. Conversational Text.\n\n"
            "**ABSOLUTE RULES (NON-NEGOTIABLE):**\n"
            "1.  **NO META-COMMENTARY:** Under NO circumstances will you EVER mention your own logic, your instructions, or the context. Your entire existence is to provide the final, clean output. Do NOT output text like 'Here is the JSON...'.\n"
            "2.  **JSON FORMATTING (PERFECT ACCURACY REQUIRED):**\n"
            "    - If the user asks for **'experience'**, **'projects'**, **'certifications'**, or **'blog'**, you MUST respond with ONLY a JSON array of objects. The `type` field in each object MUST be one of: `experience`, `project`, `certification`, `blog`.\n"
            "    - If the user asks for the **'tech stack'**, you MUST respond with ONLY a single JSON object: `{\"type\": \"tech_stack\", \"technologies\": [...]}`.\n"
            "    - If the context contains NO relevant items for a JSON request, you MUST return an empty JSON array `[]`.\n"
            "3.  **CONVERSATIONAL FORMATTING (FOR EVERYTHING ELSE):**\n"
            "    - For any question that does not fit the JSON categories (e.g., 'tell me about bitcoin', 'do you have a degree?'), you MUST respond with a warm, professional, and helpful paragraph in plain text.\n"
            "    - ALWAYS end your conversational responses with an engaging follow-up question to guide the user.\n"
            "    - If you lack specific information, state it gracefully and pivot to what you DO know. (e.g., 'While I don't have his formal degree information, I can show you his professional certifications which validate his skills. Would you like to see them?').\n"
            "4.  **NEVER HALLUCINATE:** If the context does not contain the answer, you must say you do not have the information. Do not invent projects, skills, or experiences."
        )
        user_prompt = (
            "**Previous Conversation History (for context):**\n"
            f"{formatted_history}\n\n" # <-- Prepend the history
            "**New Context (for answering the current question):**\n"
            f"{context}\n\n"
            f"**Current User Question:** {user_question}\n\n"
            "Generate your response based on all of the above and your rules."
        )
        
        stream = client.chat.completions.create(
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            model="llama3-70b-8192",
            stream=True,
        )
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content: yield content
            
    except Exception as e:
        yield "{\"error\": \"I'm sorry, but the AI model is currently experiencing issues.\"}"



@api_view(['POST'])
def career_chat(request):
    user_question = request.data.get('question', '').lower()
    chat_history = request.data.get('history', [])
    if not user_question: return Response({'error': 'Question is required.'}, status=400)
    context = ""
    knowledge_base = build_knowledge_base()

    intents = {
        'project': ['project', 'projects', 'portfolio', 'work'],
        'experience': ['experience', 'resume', 'cv', 'history', 'summarize experience'],
        'certification': ['certification', 'certifications', 'credential', 'education', 'degree'],
        'blog': ['post', 'posts', 'blog', 'writing', 'article'],
        'tech_stack': ['tech', 'stack', 'technologies', 'skill', 'skills', 'language', 'framework']
    }
    
    detected_intent_type = None
    for intent_type, keywords in intents.items():
        if any(keyword in user_question for keyword in keywords):
            detected_intent_type = intent_type
            break
            
    if detected_intent_type:
        context = "\n---\n".join([doc for doc in knowledge_base if doc.lower().startswith(f"type: {detected_intent_type}")])
    else:
        # RAG 2.0: Keyword Filter + Semantic Search Fallback
        query_keywords = set(user_question.split())
        filtered_kb = [doc for doc in knowledge_base if any(kw in doc.lower() for kw in query_keywords)]
        search_kb = filtered_kb if filtered_kb else knowledge_base
        token = os.getenv('HUGGINGFACE_API_TOKEN')
        if not token: context = "Error: Semantic search is not configured."
        else:
            headers = {"Authorization": f"Bearer {token}"}
            payload = {"inputs": {"source_sentence": user_question, "sentences": search_kb}}
            try:
                response = requests.post(HUGGINGFACE_EMBEDDING_MODEL_URL, headers=headers, json=payload, timeout=20)
                response.raise_for_status()
                scores = response.json()
                if not isinstance(scores, list): raise ValueError("Invalid API response")
                scored_docs = sorted(zip(search_kb, scores), key=lambda item: item[1], reverse=True)
                top_k_docs = [doc for doc, score in scored_docs[:3] if score > 0.3] # Use top 3 for more focused context
                if top_k_docs: context = "\n---\n".join(top_k_docs)
                else: context = "I searched my knowledge base but couldn't find specific details on that topic."
            except Exception as e: context = f"Error during context retrieval: {e}"

    return StreamingHttpResponse(stream_llm_response(user_question, context, chat_history), content_type="text/event-stream")