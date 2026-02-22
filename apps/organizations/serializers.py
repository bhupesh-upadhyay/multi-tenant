# myapp/serializers.py
from rest_framework import serializers
from .models import Organization

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['name', 'slug', 'owner', 'plan']
        read_only_fields = ('owner', 'plan')
