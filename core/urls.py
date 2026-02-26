"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from apps.organizations.views import OrganizationViewSet
from apps.projects.views import ProjectViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from debug_toolbar.toolbar import debug_toolbar_urls

router = DefaultRouter()
router.register(r'org', OrganizationViewSet, basename='organization') # TODO: why need basename

"""
# Nested routers of Project
projects_router =  NestedDefaultRouter(router, r'org', lookup='organization')
projects_router.register(r'projects', ProjectViewSet, basename='project')
ß"""
    
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('api/org/<int:org_id>/projects/', ProjectViewSet.as_view({"get":"list", "post":"create"})),
    path('api/org/<int:org_id>/projects/<int:pk>/', ProjectViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}))
] + debug_toolbar_urls()
