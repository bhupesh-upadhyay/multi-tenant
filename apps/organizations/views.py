# myapp/views.py
from rest_framework import viewsets, permissions
from .models import Organization, Membership
from .serializers import OrganizationSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from .services import create_organization
from .permissions import IsOrgRoleAllowed

class OrganizationViewSet(viewsets.ModelViewSet):
    # Never expose global queryset in multi-tenant systems.
    # queryset = Organization.objects.none() # to avoid the routers error:
    serializer_class = OrganizationSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOrgRoleAllowed]
    
    def get_queryset(self):
        """
        Only the apporiate user can Put and Patch the Organisation.
        checks if Current user is the member of the organisation
        """
        return Organization.objects.filter(memberships__user=self.request.user).distinct() # TODO: select_related("owner") prefetch_related("memberships")
        
    def perform_create(self, serializer):
        """
        Any Authenticated user can create org will be Owner of the Org,
        And becomes a member at the same time with Role = OWNER
        """
        org = create_organization(
            owner=self.request.user,
            name=serializer.validated_data["name"],
            slug=serializer.validated_data.get("slug", None)
        )
        # Instead of serializer.save() we are just assigning new org obj to serzer instance bcoz obj.save() is already happeing in service.
        serializer.instance = org
