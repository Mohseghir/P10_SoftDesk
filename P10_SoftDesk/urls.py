
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
    path('api/signup/', RegisterAPIView.as_view(), name='signup'),
    path('api/login/', TokenObtainPairView.as_view(), name='token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls))

]
"""from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib import admin
from django.urls import path, include

from api.views import ProjectViewSet, ContributorViewSet, RegisterAPIView,\
    IssueViewSet, CommentViewSet

projects_router = routers.SimpleRouter(trailing_slash=False)
projects_router.register(r"projects/?", ProjectViewSet)
users_router = routers.NestedSimpleRouter(
    projects_router, r"projects/?", lookup="projects", trailing_slash=False
)
users_router.register(r"users/?", ContributorViewSet, basename="users")
issues_router = routers.NestedSimpleRouter(
    projects_router, r"projects/?", lookup="projects", trailing_slash=False
)
issues_router.register(r"issues/?", IssueViewSet, basename="issues")
comments_router = routers.NestedSimpleRouter(
    issues_router, r"issues/?", lookup="issues", trailing_slash=False
)
comments_router.register(r"comments/?", CommentViewSet, basename="comments")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(projects_router.urls)),
    path("", include(users_router.urls)),
    path("", include(issues_router.urls)),
    path("", include(comments_router.urls)),
    path("signup/", RegisterAPIView.as_view()),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
]"""


