"""
URL configuration for tasktracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from rest_framework_nested import routers
from users.views import SignupView, UserDetail, UserListView
from projects.views import ProjectViewSet, ContributorViewSet
from issues.views import IssueViewSet, CommentViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = routers.SimpleRouter()
router.register(r'projects', ProjectViewSet)  # Creates standard CRUD routes for projects

# Nested router for projects, allowing for the inclusion of contributor and issue routes under each project
projects_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
projects_router.register(r'users', ContributorViewSet, basename='project-users') # Routes for Contributors within a Project
projects_router.register(r'issues', IssueViewSet, basename='project-issues')  # Routes for Issues within a Project

# Further nested router for issues, creating routes for comments under each issue
issues_router = routers.NestedSimpleRouter(projects_router, r'issues', lookup='issue')
issues_router.register(r'comments', CommentViewSet, basename='issue-comments') # Routes for Comments within an Issue

# URL patterns defining the accessible routes in the application
urlpatterns = [
    path('admin/', admin.site.urls), # Admin panel URL
    path('signup/', SignupView.as_view(), name='signup'), # Signup URL for new users
    path('users/', UserListView.as_view(), name='user-list'), # URL for listing users
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'), # URL for user detail, update, delete
    path('', include(router.urls)), # Include routes from the root router
    path('', include(projects_router.urls)), # Include project nested router URLs
    path('', include(issues_router.urls)), # Include issue nested router URLs
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # URL for obtaining JWT token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # URL for refreshing JWT token
]