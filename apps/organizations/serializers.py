# myapp/serializers.py
from rest_framework import serializers
from .models import Organization, Membership

class OrganizationSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False)
    class Meta:
        model = Organization
        fields = ['name', 'slug', 'owner', 'plan', 'id']
        read_only_fields = ('owner', 'plan', "id")

# TODO: Membership serializer
"""        
class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
"""