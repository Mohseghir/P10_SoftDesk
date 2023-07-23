
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_nested.routers import NestedSimpleRouter

from api.views import ProjectViewSet, ContributorViewSet, RegisterAPIView,\
    IssueViewSet, CommentViewSet

router = routers.SimpleRouter()

router.register('projects', ProjectViewSet, basename='projects')
"""router.register('comments', CommentViewSet, basename='comments')
router.register('issues', IssueViewSet, basename='issues')
router.register('users', ContributorViewSet, basename='users')"""


projects_router = NestedSimpleRouter(router, 'projects', lookup='project')
projects_router.register('users', ContributorViewSet, basename='projects-users')
## generates:
# api/project/{project_id}/users/
# api/project/{project_id}/users/{users_id}/

projects_router.register('issues', IssueViewSet, basename='projects-issues')
## generates:
# api/project/{project_id}/issues/
# api/project/{project_id}/issues/{issues_id}/

issues_router = NestedSimpleRouter(projects_router, 'issues', lookup='issue')
issues_router.register('comments', CommentViewSet, basename='projects-issues-comments')
## generates:
# api/project/{project_id}/issues/{issues_id}/comments/
# api/project/{project_id}/issues/{issues_id}/comments/{comments_id}/

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('', include(projects_router.urls)),
    path('', include(issues_router.urls)),
    path('signup/', RegisterAPIView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token'),
]
"""urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(projects_router.urls)),
    path("", include(users_router.urls)),
    path("", include(issues_router.urls)),
    path("", include(comments_router.urls)),
    path("signup/", RegisterAPIView.as_view()),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
]"""


