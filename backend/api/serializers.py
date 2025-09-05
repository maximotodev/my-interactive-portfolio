# backend/api/serializers.py
from rest_framework import serializers
from .models import ContactSubmission, Project, Certification, Post, WorkExperience, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'slug']

class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
        # This will include the full tag object (name and slug) in the project data.
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = '__all__'

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
            # This will include the full tag object (name and slug) in the project data.
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = '__all__'
        lookup_field = 'slug'

class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'subject', 'message'] # Only these fields are needed from the user