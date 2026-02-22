from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from .models import Organization, Membership
from django.utils.text import slugify

def create_organization(owner, name, slug=None):
    # 1. Check plan limit
    if owner.owned_organizations.count() >= 3:
        raise  ValidationError("Buy Plan to create More Organisations") # TODO: PermissionDenied
    if slug:
        if Organization.objects.filter(slug=slug).exists():
            raise IntegrityError("slug already exist")
    else:
        # 2. Generate slug if needed
        base_slug = slugify(name.strip().lower())
        slug=base_slug
        counter = 1
        while Organization.objects.filter(slug=slug).exists():
            # 3. Ensure slug uniqueness (decide strategy)
            slug = f"{base_slug}-{counter}"
            counter += 1
    # 4. with transaction.atomic():
    with transaction.atomic():
        # create organization
        org = Organization.objects.create(owner=owner, name=name, slug=slug)
        # create owner membership
        Membership.objects.create(role='OWNER', user=owner, organization=org)
        # 5. return organization
        return org