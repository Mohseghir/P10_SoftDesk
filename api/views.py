from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
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
                            " Now perform Login to get your token"),
            }
        )


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    queryset = Projects.objects.all()
    http_method_names = ["get", "post", "put", "delete"]

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author"] = request.user.pk
        request.POST._mutable = False
        return super(ProjectViewSet, self).create(request, *args, **kwargs)

    #  création de requête complexe avec l'objet Q en combinant des expressions logiques
    # filtrer les objets de l'auteur OR les objets du contributeur
    def get_queryset(self):
        return Projects.objects.filter(
            Q(author=self.request.user.id) | Q(contributors__user=self.request.user.id)
        )

    # contributors__user_id fait référence à une relation "Many-to-many"
    # entre les modèles Project et Contributor
    def update(self, request, *args, **kwargs):
        return super(ProjectViewSet, self).update(request, *args, **kwargs)
    # Assigner un contributeur à un projet


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorsSerializer
    permission_classes = [IsAuthenticated]
    queryset = Contributors.objects.all()
    http_method_names = ["get", "post", "delete"]

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["project"] = self.kwargs["project_pk"]
        request.POST._mutable = False
        return super(ContributorViewSet, self).create(request, *args, **kwargs)

    # filtrer les contributeurs en fonction de l'ID du projet,
    # qui est extrait de self.kwargs['project_pk']
    def get_queryset(self):
        return Contributors.objects.filter(project=self.kwargs["project_pk"])
    #  Récupérer le projet correspondant à l'ID du projet transmis dans l'URL.
    #  J'ai utilisé get_object_or_404 pour récupérer l'objet Projects ou renvoyer une erreur 404
    #  si le projet n'existe pas. Ensuite, j'ai sauvegardé le contributeur en utilisant serializer
    #  .save(project_id=project) et renvoyé la réponse avec les données du contributeur créé.


class IssueViewSet(ModelViewSet):
    serializer_class = IssuesSerializer
    permission_classes = [IsAuthenticated]
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
        request.POST._mutable = True
        request.data["project"] = self.kwargs["project_pk"]
        request.data["author"] = request.user.pk
        request.data["assigned_user"] = request.user.pk
        request.POST._mutable = False
        return super(IssueViewSet, self).update(request, *args, **kwargs)


class CommentViewSet(ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = [IsAuthenticated]

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
