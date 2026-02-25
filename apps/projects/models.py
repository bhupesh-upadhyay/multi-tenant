from django.db import models
from apps.common.models import SoftDeleteModel
from apps.organizations.models import Organization
from django.contrib.auth.models import User
# Create your models here.

class Project(SoftDeleteModel):
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('ARCHIVED', 'Archived'),
        ('COMPLETED', 'Completed'),
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='projects')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='created_projects', null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "name"],
                name="unique_project_name_per_org"
            ),
            models.UniqueConstraint(
                fields=["organization", "slug"],
                name="unique_project_slug_per_org"
            ),
        ]
        indexes = [
            models.Index(fields=["organization"]),
            models.Index(fields=["status"]),
            models.Index(fields=["slug"]),
        ]   
        