from rest_framework import permissions
import logging
logger = logging.getLogger(__name__)

class IsOrgRoleAllowed(permissions.BasePermission):

    """
    Custom permission based on user membership role and action.
    """
    # TODO: Implement has_permission() for create Action
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        logger.warning(f"User: {user}")
        # Get membership role for this org + user
        membership = obj.memberships.filter(user=user).first()
        logger.warning(f"membership: {membership}")
        if not membership:
            return False  # user not part of org

        role = membership.role
        if request.method in permissions.SAFE_METHODS:
            return role in ["OWNER", "ADMIN", "MEMBER"]

        if view.action in ["update", "partial_update"]:
            return role in ["OWNER", "ADMIN"]

        if view.action == "destroy":
            return role == "OWNER"

        return False


# Membership role based permission
"""
Not Global Permission instead Action based Permission
Action	  | Required Role
list	  | Member+
retrieve. | Member+
update	  | Admin+
destroy	  | Owner only
"""

# Permission Analogy
"""
This is where we need precision.
In DRF, permissions work at two levels:
🔹 has_permission()
Runs BEFORE object is fetched
Used for:
Authentication checks
General access rules
🔹 has_object_permission()
Runs AFTER object is fetched
Used for:
Role-based access
Object-level rules
For role-based SaaS control, we need:
👉 has_object_permission()
Because:
We must check role against THIS specific organization.
Role differs per organization.
Same user may be ADMIN in org A and MEMBER in org B.
So this is NOT global.
This is object-level permission.
"""