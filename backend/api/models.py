# backend/api/models.py
from django.db import models

class WorkExperience(models.Model):
    company_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text="Leave blank if this is your current position")
    responsibilities = models.TextField(help_text="Enter each responsibility on a new line. They will be formatted as bullet points.")
    
    class Meta:
        ordering = ['-start_date'] # Show newest jobs first

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

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
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)