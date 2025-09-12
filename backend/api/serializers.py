# backend/api/serializers.py
from rest_framework import serializers
# --- UPDATED IMPORTS ---
from .models import (
    ContactSubmission, Project, Certification, Post, 
    WorkExperience, Tag, Stall, Product # <-- Import Stall and Product
)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'slug']

class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = '__all__'

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = '__all__'
        lookup_field = 'slug'

class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'subject', 'message']

# --- NEW: Stall and Product Serializers ---
class StallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stall
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    # We can nest the stall's data within the product for a richer API response
    stall = StallSerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'

# --- REMOVED: The old ListingSerializer class ---
# class ListingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Listing
#         fields = '__all__'