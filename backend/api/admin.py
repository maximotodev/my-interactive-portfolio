# backend/api/admin.py
from django.contrib import admin
from .models import ContactSubmission, Project, Certification, Post, WorkExperience, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    # This will automatically create the URL-friendly slug from the name field
    prepopulated_fields = {'slug': ('name',)}

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company_name', 'start_date', 'end_date')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'repository_url', 'live_url')
    search_fields = ('title', 'description', 'tags__name')
    filter_horizontal = ('tags',)


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
    filter_horizontal = ('tags',)

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject', 'message')
    # Make the message content read-only in the admin list view
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')