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