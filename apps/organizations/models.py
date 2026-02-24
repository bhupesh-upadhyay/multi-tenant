from django.db import models
from django.contrib.auth.models import User
from apps.common.models import SoftDeleteModel


class Organization(SoftDeleteModel):
    PLAN_CHOICES = (
        ("FREE", "Free"),
        ("PRO", "Pro"),
        ("ENTERPRISE", "Enterprise"),
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_organizations"
    )
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default="FREE")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["owner"]),
        ]

    def __str__(self):
        return self.name
    
class Membership(SoftDeleteModel):
    ROLE_CHOICES = (
        ("OWNER", "Owner"),
        ("ADMIN", "Admin"),
        ("MEMBER", "Member"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="memberships"
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="memberships"
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "organization")
        indexes = [
            models.Index(fields=["organization"]),
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.organization.name}"

"""
Why owner is stored in Organization AND Membership?
Because:
Organization.owner → quick access
Membership → permission control
Owner will ALSO have membership with role OWNER
"""