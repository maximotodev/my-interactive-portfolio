# backend/api/admin.py
from django.contrib import admin
from .models import Project, Certification, Post, WorkExperience

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company_name', 'start_date', 'end_date')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'technologies', 'repository_url', 'live_url')
    search_fields = ('title', 'description', 'technologies')

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'issuing_organization', 'date_issued')
    list_filter = ('issuing_organization', 'date_issued')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published_date', 'is_published')
    list_filter = ('is_published', 'published_date')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}