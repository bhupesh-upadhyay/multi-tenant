from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required = False)
    class Meta:
        model = Project
        fields = ['id', 'organization', 'status', 'name', 'slug', 'description', 'created_at']
        read_only_fields = ['id', 'organization', 'status', 'created_at', 'updated_at', 'created_by']