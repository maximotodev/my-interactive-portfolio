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
from groq import Groq

# Local Imports
from .models import Project, Certification, Post
from .serializers import ProjectSerializer, CertificationSerializer, PostSerializer

# --- Configuration Constants ---
GITHUB_USERNAME = "maximotodev"
NOSTR_RELAYS = ["wss://relay.damus.io", "wss://relay.primal.net", "wss://nos.lol", "wss://relay.nostr.band"]
CACHE_TIMEOUT_SECONDS = 3600  # 1 hour
BITCOIN_WALLET_NAME = "MyPortfolioWallet"
HUGGINGFACE_EMBEDDING_MODEL_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
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

# --- AI SKILL MATCHER 2.0 (API-POWERED) ---
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
        
        # Prepare the payload for the Sentence Similarity task
        payload = {
            "inputs": {
                "source_sentence": query,
                "sentences": project_docs
            }
        }
        
        response = requests.post(HUGGINGFACE_EMBEDDING_MODEL_URL, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        scores = response.json() # This will be a list of similarity scores

        if not isinstance(scores, list):
            # The API can sometimes return a dictionary with an error message
            print(f"Unexpected response from Hugging Face API: {scores}")
            raise ValueError("Invalid response format from embedding API.")

        results = sorted(zip(project_ids, scores), key=lambda item: item[1], reverse=True)
        
        ranked_projects = [{'id': pid, 'score': float(score)} for pid, score in results if score > 0.3]
        return Response(ranked_projects)

    except Exception as e:
        print(f"Error calling Hugging Face API: {e}")
        # If the AI service fails, fall back to a simple keyword search.
        # This makes the feature more resilient.
        keywords = query.lower().split()
        matched_ids = set()
        for p in projects:
            project_text = f"{p.title} {p.technologies}".lower()
            if any(keyword in project_text for keyword in keywords):
                matched_ids.add(p.id)
        
        fallback_projects = [{'id': pid, 'score': 1.0} for pid in matched_ids]
        return Response(fallback_projects)

# In backend/api/views.py, replace the entire career_chat function

@api_view(['POST'])
def career_chat(request):
    """
    Handles a chat request using a Retrieval-Augmented Generation (RAG) pattern
    with an improved, more granular knowledge base and a "storyteller" persona.
    """
    user_question = request.data.get('question', '')
    if not user_question:
        return Response({'error': 'Question is required.'}, status=400)

     # --- 1. KNOWLEDGE BASE CREATION (Comprehensive & Granular) ---
    projects = Project.objects.all()
    posts = Post.objects.filter(is_published=True)
    
    knowledge_base_docs = []

    # --- A. High-Level Professional Summary ---
    knowledge_base_docs.append(
        "Professional Summary: Maximoto is an AI/ML Engineer with a strong focus on full-stack development. "
        "He is a seasoned Bitcoin maximalist with a deep understanding of its foundational principles. "
        "He is currently advancing his expertise by enrolling in the IBM AI Engineering Professional Certificate program."
    )

    # --- B. Work Experience from Resume ---
    knowledge_base_docs.append(
        "Work Experience at Tribe BTC (Frontend Developer, Sep 2023 - Feb 2024): "
        "Revamped a legacy HTML/CSS/JS project into a dynamic React application, which boosted user engagement by 40% using animations and carousels. "
        "Optimized API requests with Axios, reducing data load times by 50% through techniques like skeleton loading and pagination. "
        "Streamlined team collaboration with Git/GitHub, decreasing merge conflicts by 35%. "
        "Initiated and implemented deployment automation, which slashed deployment durations by 50% and minimized errors by 75%."
    )
    knowledge_base_docs.append(
        "Work Experience as a Freelance FullStack Developer (Mar 2023 - Present): "
        "Designs and executes professional websites using HTML5, CSS3, and React, achieving 97% client satisfaction. "
        "Secured 20% more contracts by boosting client organic search traffic by 35% through advanced SEO strategies. "
        "Communicates effectively with clients through various channels including email and video conferencing."
    )

    # --- C. Detailed AI/ML Skills from IBM Certificate ---
    knowledge_base_docs.append(
        "Current Education (IBM AI Engineering Professional Certificate): "
        "This program is designed for data scientists, ML engineers, and software engineers. "
        "Built, trained, and deployed various deep learning architectures."
    )
    knowledge_base_docs.append(
        "Specific Deep Learning Skills (IBM Certificate): "
        "Gained hands-on experience with Convolutional Neural Networks (CNNs), Recurrent Networks (RNNs), Autoencoders, and Generative AI models including Large Language Models (LLMs)."
    )
    knowledge_base_docs.append(
        "Machine Learning Concepts Mastery (IBM Certificate): "
        "Mastered both supervised and unsupervised learning using Python with popular libraries like SciPy, ScikitLearn, Keras, PyTorch, and TensorFlow."
    )
    knowledge_base_docs.append(
        "Applied AI/ML Project Experience (IBM Certificate): "
        "Applied machine learning to industry problems involving object recognition, computer vision, text analytics, Natural Language Processing (NLP), and recommender systems. "
        "Built Generative AI applications using LLMs and Retrieval-Augmented Generation (RAG) with frameworks like Hugging Face and LangChain."
    )
    knowledge_base_docs.append(
        "LLM Development Experience (IBM Certificate): "
        "Created and worked with LLMs like GPT and BERT. Developed transfer learning applications in NLP using LangChain, Hugging Face, and PyTorch. "
        "Understands core concepts like positional encoding, masking, and the attention mechanism for document classification."
    )
    knowledge_base_docs.append(
        "Practical AI Application Development (IBM Certificate): "
        "Has experience setting up a Gradio interface for model interaction and constructing a Question-Answering bot using LangChain to answer questions from loaded documents."
    )

    # --- D. Other Certificates from Resume ---
    knowledge_base_docs.append("Certificate: Google AI Essentials - Learned foundations of AI, machine learning, and ethical considerations. Applied AI tools to automate tasks.")
    knowledge_base_docs.append("Certificate: Foundations of Cybersecurity (Google via Coursera) - Gained a strong understanding of core cybersecurity principles, including threat modeling, risk management, and incident response.")
    knowledge_base_docs.append("Certificate: Google Professional Certificate - Used Python and Bash for automation scripts. Learned Object-Oriented Programming, Git/GitHub, Google Cloud fundamentals, and Puppet configuration management.")
    knowledge_base_docs.append("Certificate: Scrimba Frontend Developer Career Path - Gained a well-rounded skill set in modern tooling like React and GitHub, alongside best practices in semantic HTML, JavaScript, and accessibility.")

    # --- E. Project and Blog Post Data ---
    for p in projects:
        knowledge_base_docs.append(f"Regarding the portfolio project '{p.title}': its purpose is {p.description}, and the technologies used were {p.technologies}.")
    for post in posts:
        knowledge_base_docs.append(f"From the blog post titled '{post.title}': {post.content[:700]}")



    # --- 2. RETRIEVAL (With Improved Error Handling) ---
    token = os.getenv('HUGGINGFACE_API_TOKEN')
    context = "" # Start with an empty context

    if not token:
        # If the token is missing, we can't do retrieval. Set a specific error context.
        print("ERROR: HUGGINGFACE_API_TOKEN is not set.")
        context = "Error: The semantic search feature is not configured correctly because the Hugging Face API token is missing."
    else:
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"inputs": {"source_sentence": user_question, "sentences": knowledge_base_docs}}
        
        try:
            response = requests.post(HUGGINGFACE_EMBEDDING_MODEL_URL, headers=headers, json=payload, timeout=20)
            response.raise_for_status()
            scores = response.json()

            if not isinstance(scores, list):
                # Handle cases where the API returns an error message
                print(f"ERROR: Unexpected response from Hugging Face API: {scores}")
                raise ValueError("Invalid response format from embedding API.")
            
            scored_docs = sorted(zip(knowledge_base_docs, scores), key=lambda item: item[1], reverse=True)
            top_k_docs = [doc for doc, score in scored_docs[:5] if score > 0.3]
            
            if top_k_docs:
                context = "\n---\n".join(top_k_docs)
            else:
                # This now becomes a more specific message
                context = "I searched through Maximoto's resume, projects, and writings, but I couldn't find a specific document that directly answers your question."
                
        except Exception as e:
            print(f"ERROR: An error occurred while calling the Hugging Face API: {e}")
            # Provide a very specific error context to the LLM
            context = "Error: The connection to the semantic search service (Hugging Face API) failed. Please inform the site administrator."

    # --- 3. AUGMENTATION & 4. GENERATION (This is where we make the improvements) ---
    try:
        client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        
        # --- NEW, REFINED "STORYTELLER" SYSTEM PROMPT ---
        system_prompt = (
            "You are 'Maxi', a professional and friendly AI assistant representing Maximoto, a skilled Full-Stack and AI Engineer. "
            "Your primary goal is to help recruiters and potential clients understand Maximoto's skills and experience by having a natural conversation. "
            "Follow these rules strictly:\n"
            "1.  **Synthesize, Don't List:** Do not just list facts from the context. Weave the information from the provided 'Context' into a smooth, conversational paragraph. Use full sentences.\n"
            "2.  **Be a Storyteller:** Instead of saying 'The context says...', narrate the information. For example, instead of 'Work Experience at Tribe BTC...', say 'At Tribe BTC, Maximoto took the lead on...'\n"
            "3.  **Strictly Use Context:** Base your answers ONLY on the provided 'Context'. If the information is not in the context, politely state that you don't have details on that specific topic.\n"
            "4.  **Organize Information:** When asked about broad topics like 'skills' or 'experience', use Markdown headings (like `### Frontend Development`) to organize the information clearly.\n"
            "5.  **Be Personable:** Maintain a helpful and professional tone. You are here to help people learn about Maximoto."
        )

        # --- SLIGHTLY REFINED USER PROMPT ---
        user_prompt = (
            f"Please use the following context to answer my question. Remember to follow all the rules in your system prompt.\n\n"
            f"**Context:**\n{context}\n\n"
            f"**My Question:** {user_question}"
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama3-8b-8192", # This model is excellent at following instructions
        )
        
        ai_response = chat_completion.choices[0].message.content
        return Response({"answer": ai_response})

    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return Response({'error': 'Failed to generate a response from the AI model.'}, status=502)