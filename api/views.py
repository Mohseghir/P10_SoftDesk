from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
"""from .permissions import IsContributorOrAuthorProjectInComments,\
    IsContributorOrAuthorInProjects, IsContributorOrAuthor"""
from . permissions import PermissionProjectView, \
    PermissionContributorView, PermissionIssueView,\
    PermissionCommentView

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from api.models import Projects, Contributors, Issues, Comments
from api.serializers import ProjectSerializer, ContributorsSerializer, \
    RegisterSerializer, IssuesSerializer, CommentsSerializer, UserSerializer

# Create your views here.


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "message": ("User Created Successfully.",
                            " Please Login to get your access token"),
            }
        )


class ProjectViewSet(ModelViewSet):
    # Spécification du sérialiseur
    serializer_class = ProjectSerializer
    # Classes de permission à appliquer
    permission_classes = [IsAuthenticated, PermissionProjectView]
    # Définition du queryset pour récupérer tous les objets Project de la base de données
    queryset = Projects.objects.all()
    # Méthodes HTTP autorisées pour cette vue
    http_method_names = ["get", "post", "put", "delete"]

    def create(self, request, *args, **kwargs):
        # Surcharge de la méthode create pour ajouter l'ID de l'auteur au projet avant la création
        request.POST._mutable = True
        request.data["author"] = request.user.pk
        request.POST._mutable = False
        return super(ProjectViewSet, self).create(request, *args, **kwargs)
########
    def get_queryset(self):
        # Surcharge de la méthode get_queryset pour filtrer les projets en fonction de l'utilisateur
        return Projects.objects.filter(
            Q(author=self.request.user.id) | Q(contributors__user=self.request.user.id)
        ).distinct()

    def update(self, request, *args, **kwargs):
        # Surcharge de la méthode update pour mettre à jour un projet existant
        return super(ProjectViewSet, self).update(request, *args, **kwargs)


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorsSerializer
    permission_classes = [IsAuthenticated, PermissionContributorView]
    queryset = Contributors.objects.all()
    http_method_names = ["get", "post", "delete"]

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["project"] = self.kwargs["project_pk"]
        request.POST._mutable = False
        return super(ContributorViewSet, self).create(request, *args, **kwargs)

    def get_queryset(self):
        return Contributors.objects.filter(project=self.kwargs["project_pk"])


class IssueViewSet(ModelViewSet):
    serializer_class = IssuesSerializer
    permission_classes = [IsAuthenticated, PermissionIssueView]
    queryset = Issues.objects.all()
    http_method_names = ["get", "post", "put", "delete"]

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["project"] = self.kwargs["project_pk"]
        request.data["author"] = request.user.pk
        request.data["assigned_user"] = request.user.pk
        request.POST._mutable = False
        return super(IssueViewSet, self).create(request, *args, **kwargs)

    def get_queryset(self):
        return Issues.objects.filter(project=self.kwargs["project_pk"])

    def update(self, request, *args, **kwargs):
        # Surcharge de la méthode update pour définir les valeurs des champs
        # avant la mise à jour de l'objet Issue
        request.POST._mutable = True
        # On définit la valeur du champ "project" avec la valeur passée dans
        # les paramètres de l'URL, project_pk. Cela permet d'associer l'issue au projet spécifié.
        request.data["project"] = self.kwargs["project_pk"]
        # On définit la valeur du champ "author" avec l'ID de l'utilisateur actuel
        request.data["author"] = request.user.pk
        # On définit la valeur du champ "assigned_user" avec
        # l'ID de l'utilisateur actuel (request.user.pk). Cela permet d'assigner
        # l'issue à l'utilisateur actuel.
        request.data["assigned_user"] = request.user.pk
        request.POST._mutable = False
        return super(IssueViewSet, self).update(request, *args, **kwargs)


class CommentViewSet(ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = [IsAuthenticated, PermissionCommentView]

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author_user_id"] = request.user.pk
        request.data["issue_id"] = self.kwargs["issue_pk"]

        request.POST._mutable = False
        return super(CommentViewSet, self).create(request, *args, **kwargs)

    def get_queryset(self):
        return Comments.objects.filter(issue_id=self.kwargs["issue_pk"])

    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author_user_id"] = request.user.pk
        request.data["issue_id"] = self.kwargs["issue_pk"]
        request.POST._mutable = False
        return super(CommentViewSet, self).update(request, *args, **kwargs)
