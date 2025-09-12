# backend/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# --- UPDATED IMPORTS ---
from .views import (
    ProjectViewSet,
    CertificationViewSet,
    PostViewSet,
    WorkExperienceViewSet,
    TagViewSet,
    StallViewSet,    # <-- ADD THIS
    ProductViewSet,  # <-- ADD THIS
    github_stats,
    github_contributions,
    nostr_profile,     
    latest_note,
    bitcoin_address,
    mempool_stats,
    skill_match_view,
    career_chat,
    search_view,
    contact_form_submit,
    nostr_contact_submit,
)

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'certifications', CertificationViewSet)
router.register(r'posts', PostViewSet, basename='post')
router.register(r'work-experience', WorkExperienceViewSet)
router.register(r'tags', TagViewSet) 
# --- NEW ROUTER REGISTRATIONS ---
router.register(r'stalls', StallViewSet)
router.register(r'products', ProductViewSet)
# --- REMOVED OLD ROUTER ---
# router.register(r'listings', ListingViewSet) # This line was causing the error

urlpatterns = [
    path('', include(router.urls)),
    path('search/', search_view, name='search'),
    path('github-stats/', github_stats, name='github-stats'),
    path('github-contributions/', github_contributions, name='github-contributions'),
    path('nostr-profile/', nostr_profile, name='nostr-profile'), 
    path('latest-note/', latest_note, name='latest-note'),
    path('mempool-stats/', mempool_stats, name='mempool-stats'),
    path('bitcoin-address/', bitcoin_address, name='bitcoin-address'),
    path('skill-match/', skill_match_view, name='skill-match'),
    path('chat/', career_chat, name='career-chat'),  
    path('contact/', contact_form_submit, name='contact-submit'),
    path('nostr-contact/', nostr_contact_submit, name='nostr-contact-submit'),
]