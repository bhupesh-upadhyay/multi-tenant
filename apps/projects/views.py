from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from apps.common.mixins import TenantResolutionMixin
from .serializers import ProjectSerializer
from .models import Project
from .services import create_project

# Create your views here.
class ProjectViewSet(TenantResolutionMixin, ModelViewSet):
    serializer_class = ProjectSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        org = self.get_organization()
        return Project.objects.filter(organization=org)

    def perform_create(self, serializer):
        org = self.get_organization()
        project = create_project(
            organization=org,
            created_by=self.request.user,
            name=serializer.validated_data["name"],
            slug=serializer.validated_data.get("slug"),
            description=serializer.validated_data.get("description", "")
        )
        print(project)
        serializer.instance = project