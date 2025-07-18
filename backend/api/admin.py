# backend/api/admin.py

from django.contrib import admin
from .models import Project, Certification, Post # Import your models

# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Customizes the display of the Project model in the admin panel.
    """
    list_display = ('title', 'technologies', 'repository_url', 'live_url')
    search_fields = ('title', 'description', 'technologies')

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    """
    Customizes the display of the Certification model in the admin panel.
    """
    list_display = ('name', 'issuing_organization', 'date_issued')
    list_filter = ('issuing_organization', 'date_issued')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published_date', 'is_published')
    list_filter = ('is_published', 'published_date')
    search_fields = ('title', 'content')
    # This will automatically pre-populate the slug field from the title
    prepopulated_fields = {'slug': ('title',)}