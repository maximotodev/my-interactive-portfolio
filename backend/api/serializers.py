# backend/api/serializers.py
from rest_framework import serializers
from .models import Project, Certification

class ProjectSerializer(serializers.ModelSerializer):
    # This field will generate the full URL for the image
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Project
        fields = (
            'id', 
            'title', 
            'description', 
            'technologies', 
            'repository_url', 
            'live_url', 
            'image'
        )

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'