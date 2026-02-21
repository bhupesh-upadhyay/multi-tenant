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

