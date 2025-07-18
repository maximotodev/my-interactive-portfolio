# backend/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet, CertificationViewSet, PostViewSet, github_stats, github_contributions,
    skill_match_view, nostr_profile, bitcoin_address,
    latest_note # <-- Add this import
)

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'certifications', CertificationViewSet)
router.register(r'posts', PostViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('github-stats/', github_stats, name='github-stats'),
    path('github-contributions/', github_contributions, name='github-contributions'),
    path('skill-match/', skill_match_view, name='skill-match'),
    path('nostr-profile/', nostr_profile, name='nostr-profile'),
    path('bitcoin-address/', bitcoin_address, name='bitcoin-address'),
    path('latest-note/', latest_note, name='latest-note'), # <-- ADD THIS LINE
]