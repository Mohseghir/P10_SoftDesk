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

# routeur principal respensable des routes de première niveau pour nos urls
router = routers.SimpleRouter()
# avec la fonction register nous enregistrons ProjectViewSet sur le routeur principal
# Cela crée les routes URL pour les opérations CRUD liées aux projets
router.register('projects', ProjectViewSet, basename='projects')
# création d'un routeur imbriqué (projects_router) à partir du routeur principal
# Le paramètre lookup='project' spécifie que nous utiliserons le champ project
# pour rechercher les objets dans les vues associées.
projects_router = routers.NestedSimpleRouter(router, 'projects', lookup='project')

# nous enregistrons notre vue sur le routeur imbriqué pour créer les urls
projects_router.register('users', ContributorViewSet, basename='projects-users')

# enregistrons la vue sur les deux routeur
projects_router.register('issues', IssueViewSet, basename='projects-issues')


# Creation du routeur imbriqué (issures_router) à partir du routeur deja imbriqué (projects_routers)
# on specifi le champ "issue" pour trouver les objects dans les vues associées
issues_router = routers.NestedSimpleRouter(projects_router, 'issues', lookup='issue')
issues_router.register('comments', CommentViewSet, basename='projects-issues-comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/signup/', RegisterAPIView.as_view(), name='signup'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls))

]
