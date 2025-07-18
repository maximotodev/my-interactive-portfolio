# backend/api/models.py
from django.db import models

class Certification(models.Model):
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=100, default="Coursera")
    credential_url = models.URLField(blank=True, null=True)
    date_issued = models.DateField()

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=300, help_text="Comma-separated list of technologies")
    repository_url = models.URLField(blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    image = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, help_text="A URL-friendly version of the title. Will be auto-generated.")
    content = models.TextField(help_text="Write your blog post content using Markdown.")
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published_date'] # Show newest posts first

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-generate a slug from the title if one isn't provided
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)