from rest_framework.exceptions import ValidationError, PermissionDenied
from django.utils.text import slugify
import logging
from django.db import transaction
from .models import Project

logger = logging.getLogger(__name__)

def create_project(organization, created_by, name, slug=None, description=""): # Removed **kwargs why: Explicit > implicit.
    name = name.strip()

    logger.info(f"project detail: {name}")
    # 1. Validate name uniqueness within organization
    if Project.objects.filter(organization=organization, name=name,is_deleted=False).exists():
        raise ValidationError({"name":"name already exists"})
    
    if slug:
        slug = slugify(slug.strip().lower())
        if Project.objects.filter(slug=slug, organization=organization, is_deleted=False).exists():
            raise ValidationError({"slug": "Slug already exists."})
    # 2. Generate slug if not provided
    # 3. Ensure slug uniqueness within organization
    else:
        base_slug = slugify(name.strip().lower())
        slug=base_slug
        counter = 1
        while Project.objects.filter(slug=slug, organization=organization, is_deleted=False).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

    # 4. Best practice: wrap in atomic.:
        # create project
    """
    Because tomorrow you may add:
        Activity log
        Notification
        Task counter update
    Atomic protects future extension.
    """
    with transaction.atomic():    
        project = Project.objects.create( 
                    organization=organization,
                    name=name,
                    slug=slug,
                    description=description,
                    status="ACTIVE",
                    created_by = created_by
                )
        # 5. return project
        return project


    
    