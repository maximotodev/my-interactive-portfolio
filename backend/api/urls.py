# backend/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet,
    CertificationViewSet,
    PostViewSet,
    WorkExperienceViewSet,
    github_stats,
    github_contributions,
    nostr_profile,
    latest_note,
    bitcoin_address,
    mempool_stats,
    skill_match_view,
    career_chat,
)

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'certifications', CertificationViewSet)
router.register(r'posts', PostViewSet)
router.register(r'work-experience', WorkExperienceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('github-stats/', github_stats, name='github-stats'),
    path('github-contributions/', github_contributions, name='github-contributions'),
    path('nostr-profile/', nostr_profile, name='nostr-profile'),
    path('latest-note/', latest_note, name='latest-note'),
    path('mempool-stats/', mempool_stats, name='mempool-stats'),
    path('bitcoin-address/', bitcoin_address, name='bitcoin-address'),
    path('skill-match/', skill_match_view, name='skill-match'),
    path('chat/', career_chat, name='career-chat'),    
]