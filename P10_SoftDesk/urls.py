"""
URL configuration for P10_SoftDesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_nested import routers

from api.views import ProjectViewSet, ContributorViewSet, RegisterAPIView, \
    LoginView, IssueViewSet, CommentViewSet

router = routers.SimpleRouter()

router.register('projects', ProjectViewSet, basename='projects')

project_router = routers.NestedSimpleRouter(router, r'projects', lookup='projects')
project_router.register(r'users', ContributorViewSet, basename='project-users')
## generates:
# api/project/{project_id}/users/
# api/project/{project_id}/users/{users_id}/

project_router.register(r'issues', IssueViewSet, basename='project-issues')
## generates:
# api/project/{project_id}/issues/
# api/project/{project_id}/issues/{issues_id}/

issue_router = routers.NestedSimpleRouter(project_router, r'issues', lookup='issue')
issue_router.register(r'comments', CommentViewSet, basename='project-comments')
## generates:
# api/project/{project_id}/issues/{issues_id}/comments/
# api/project/{project_id}/issues/{issues_id}/comments/{comments_id}/


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('', include(project_router.urls)),
    path('', include(issue_router.urls)),
    path('api/signup/', RegisterAPIView.as_view(), name='signup'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls))

]
