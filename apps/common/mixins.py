"""
This mixin will be reused for:
Projects
Tasks
Comments
Analytics
"""

from django.shortcuts import get_object_or_404
from apps.organizations.models import Organization

"""
Every nested tenant ViewSet must:
Extract org_id from URL
Validate user membership
Return 404 if not allowed
Make organization accessible everywhere in the view
Filter queryset by organization
That is shared behavior across multiple ViewSets

ModelViewSet → GenericViewSet → ViewSetMixin → APIView
"""
# A user can only access an Organization they are a member of.
class TenantResolutionMixin:

    def get_organization(self):
        """
        In-Memory (Per-Request) Cache
        This caches the object inside the view instance.
        Scope: One request only.
        checks: Does this object already have this attribute? Returns True or False.
        Why _organization? Leading underscore _ means "private/internal use", Not meant to be accessed externally
        
        """
        # Return cached organization if already resolved
        if hasattr(self, "_organization"):
            return self._organization

        org_id = self.kwargs.get("org_id")

        # Enforce tenant isolation using membership filtering
        """
        Only organizations where the current user has a membership.
        Is this specific organization in the allowed set?
        """
        organization = get_object_or_404(
            Organization.objects.filter(
                memberships__user=self.request.user
            ),
            id=org_id
        )

        # Cache it to avoid multiple DB queries
        self._organization = organization
        return self._organization