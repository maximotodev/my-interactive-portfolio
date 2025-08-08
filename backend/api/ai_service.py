import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Project, Certification, WorkExperience, Post

class KnowledgeBaseService:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            print("Initializing AI Knowledge Base Service (scikit-learn)...")
            cls._instance = super(KnowledgeBaseService, cls).__new__(cls)
            cls._instance.model = SentenceTransformer("all-MiniLM-L6-v2")
            cls._instance.documents = []
            cls._instance.embeddings = None
            cls._instance._build()
            print("AI Knowledge Base is ready.")
        return cls._instance

    def _build(self):
        docs = []
        frontend_url = os.getenv("FRONTEND_URL", "https://maximotodev.vercel.app")
        for exp in WorkExperience.objects.all():
            docs.append({"type": "experience", "title": exp.job_title, "company": exp.company_name, "date": f"{exp.start_date.strftime('%b %Y')} - {exp.end_date.strftime('%b %Y') if exp.end_date else 'Present'}", "responsibilities": [r.strip() for r in exp.responsibilities.splitlines() if r.strip()]})
        for p in Project.objects.all():
            docs.append({"type": "project", "title": p.title, "description": p.description, "url": p.live_url, "repo_url": p.repository_url, "technologies": [t.strip() for t in p.technologies.split(',') if t.strip()]})
        for c in Certification.objects.all():
            docs.append({"type": "certification", "name": c.name, "issuer": c.issuing_organization, "url": c.credential_url})
        for post in Post.objects.filter(is_published=True):
            docs.append({"type": "blog", "title": post.title, "content": post.content[:250] + "...", "url": f"{frontend_url}/blog/{post.slug}"})
        tech_set = set(t.strip() for p in Project.objects.all() for t in p.technologies.split(',') if t.strip())
        if tech_set:
            docs.append({"type": "tech_stack", "technologies": sorted(list(tech_set), key=str.lower)})
        docs.extend([
            {"type": "topic", "name": "Bitcoin", "content": "Maximoto is a passionate Bitcoin maximalist with deep knowledge of its principles, demonstrated by his work at Tribe BTC and the on-chain Bitcoin tipping feature in his portfolio."},
            {"type": "topic", "name": "Linux", "content": "Maximoto holds a 'Linux and SQL' certification from Coursera, validating his foundational skills in Linux environments."},
            {"type": "topic", "name": "AI/ML", "content": "Maximoto builds practical AI applications, including a semantic search Skill Matcher and this RAG-powered AI Career Assistant."},
            {"type": "topic", "name": "Rust", "content": "Maximoto's current knowledge base does not contain information about experience with the Rust programming language."},
        ])
        self.documents = docs
        doc_strings_for_embedding = [json.dumps(doc) for doc in self.documents]
        self.embeddings = self.model.encode(doc_strings_for_embedding, normalize_embeddings=True)

    def search(self, query, k=5, threshold=0.3):
        if self.embeddings is None: return []
        query_embedding = self.model.encode([query], normalize_embeddings=True)
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        top_k_indices = np.argsort(similarities)[-k:][::-1]
        results = [self.documents[i] for i in top_k_indices if similarities[i] > threshold]
        return results

    def get_all_by_type(self, doc_type):
        return [doc for doc in self.documents if doc.get("type") == doc_type]