from rest_framework import serializers
from .models import Project
from django.contrib.auth.models import User

class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]

class ProjectSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required = False, allow_blank=True) # allows slug:"" in request
    created_by = UserSummarySerializer(read_only=True)
    class Meta:
        model = Project
        fields = ['id', 'organization', 'status', 'name', 'slug', 'description', 'created_at', 'created_by']
        read_only_fields = ['id', 'organization', 'status', 'created_at', 'updated_at', 'created_by']