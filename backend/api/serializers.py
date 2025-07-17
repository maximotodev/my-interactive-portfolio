# backend/api/serializers.py
from rest_framework import serializers
from .models import Project, Certification

class ProjectSerializer(serializers.ModelSerializer):
    # By removing the explicit 'image' field definition, we allow the
    # ModelSerializer to correctly infer that it's a URLField from the model.
    class Meta:
        model = Project
        # Using '__all__' is the simplest way to include all fields from the model.
        fields = '__all__'

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'