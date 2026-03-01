Multi-Tenant Task Management SaaS API
(Think simplified backend of Asana or ClickUp)


User
   ↓
Organization
   ↓
Membership (role control)
   ↓
Project
   ↓
Task
   ↓
Comment


System Vision
One application.
Many organizations.
Each organization:
    Has members
    Has projects
    Has tasks
    Has role-based access
    Has usage limits
And data isolation is STRICT.


multi-tenant/
│
├── manage.py
├── core/                  ← Django settings
│
├── apps/
│   ├── accounts/
│   ├── organizations/
│   ├── projects/
│   ├── tasks/
│   ├── analytics/
│   └── common/
│
└── requirements.txt


accounts
Handles:
    JWT auth
    Login / Register
    Token management
    User-related endpoints
We use default User but still isolate auth logic.

2️⃣ organizations
Handles:
    Organization model
    Membership model
    Plan logic
    Invite system (later)
    Org-level permissions
This is the heart of multi-tenancy.

3️⃣ projects
Handles:
    Project model
    Project CRUD
    Org filtering
    Project permissions

4️⃣ tasks
Handles:
    Task model
    Comment model
    Status management
    Assignment logic
    Activity logs (or separate app if you want)

5️⃣ analytics
Handles:
    Aggregation queries
    Reports
    Dashboard stats
    Org metrics
Keep analytics separate → clean architecture.

6️⃣ common (or core_utils)
Handles:
    Soft delete base model
    Custom managers
    Base mixins
    Shared utilities
    Throttles
    Custom permissions base classes
VERY important for clean architecture.


Organization creation API
With:
Serializer
ViewSet
Auto-create OWNER membership
Transaction atomic safety

Request → Authentication → Permission check →
Serializer validation → Service layer →
Atomic transaction →
Create organization →
Create owner membership →
Commit →
Serialize response →
Return 201


Projects app (nested under organization)
Route will look like:
/api/orgs/{org_id}/projects/

<!-- This should not allow any member can create project in any orgination -->
{
  "name": "Secret Project",
  "organization": 5
}
<!-- prevention -->
1. organization must be read_only=True on MembershipSerializer
2. overide get_queryset() return new queryset filter with org_id from url (not enough)
    will not work for create because there is no existing object yet.
1️⃣ Extract org_id from self.kwargs
2️⃣ Fetch organization safely (using tenant-filtered queryset)
3️⃣ Inject that organization into service layer
4️⃣ Ignore anything sent in request body
So project creation must look like:
org = get_org_from_url()
create_project(organization=org, ...)
Never:
organization = serializer.validated_data["organization"]
Never trust client for tenant reference.


Feature	select_related()	prefetch_related()
Query type	SQL JOIN	Separate queries
DB hits	1	Usually 2
Works for	FK, OneToOne	M2M, reverse FK
Performance	Faster for single relation	Better for multiple related objects
Combines data	In SQL	In Python

✅ Use select_related() when:
Each object has one related object
Example: Book → Author
You want 1 SQL query
✅ Use prefetch_related() when:
Relationship returns multiple objects
Example: Store → books
Reverse ForeignKey
ManyToMany