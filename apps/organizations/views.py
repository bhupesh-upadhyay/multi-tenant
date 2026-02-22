# myapp/views.py
from rest_framework import viewsets, permissions
from .models import Organization, Membership
from .serializers import OrganizationSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from .services import create_organization


class OrganizationViewSet(viewsets.ModelViewSet):
    # queryset = Organization.objects.none() # to avoid the routers error:
    serializer_class = OrganizationSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):    
        return Organization.objects.filter(memberships__user=self.request.user).distinct()
        
    def perform_create(self, serializer):
        org = create_organization(
            owner=self.request.user,
            name=serializer.validated_data["name"],
            slug=serializer.validated_data.get("slug")
        )
        serializer.instance = org
