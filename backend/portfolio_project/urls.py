# backend/portfolio_project/urls.py

from django.contrib import admin
from django.urls import path, include
# --- ADD THESE TWO IMPORTS ---
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

# --- THIS IS THE CRITICAL FIX FOR LOCAL DEVELOPMENT ---
# This block tells Django's development server to serve media files
# ONLY when the DEBUG setting is True. In production (DEBUG=False),
# this block will be ignored, which is the correct and secure behavior.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)