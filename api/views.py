from django.contrib.auth import authenticate
from django.db import transaction, IntegrityError
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import Projects, Contributors, Issues, Comments
from api.permissions import ProjectPermission
from api.serializers import ProjectSerializer, ContributorsSerializer, \
    LoginSerializer, RegisterSerializer, IssuesSerializer, CommentsSerializer, UserSerializer


# Create your views here.


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        # Crée une instance d'UserSerializer avec les données de la requête
        serializer = self.serializer_class(data=request.data)

        # Vérifie si les données du serializer sont valides
        if serializer.is_valid():
            # Enregistre l'utilisateur dans la base de données
            user = serializer.save()

            # Génère un jeton de rafraîchissement et un jeton d'accès à l'aide de simplejwt
            refresh = RefreshToken.for_user(user)

            # Retourne une réponse avec les jetons et le code de statut HTTP 201 (Créé)
            return Response({
                'user': RegisterSerializer(user, context=self.get_serializer_context()).data,
                'message': "User created successfully."},
                status=status.HTTP_201_CREATED)

        # Si les données du serializer ne sont pas valides, retourne une réponse avec les erreurs du serializer
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        # Récupère le nom d'utilisateur et le mot de passe à partir des données de la requête
        username = request.data.get('username')
        password = request.data.get('password')

        # Authentifie l'utilisateur en utilisant le nom d'utilisateur et le mot de passe fournis
        user = authenticate(username=username, password=password)

        # Vérifie si l'authentification a réussi
        if user:
            # Génère un jeton de rafraîchissement et un jeton d'accès à l'aide de simplejwt
            serializer = self.serializer_class(user)

            # Retourne une réponse avec les jetons
            return Response({
                'message': "User logged successfully.",
            },
                status=status.HTTP_200_OK
            )

        # Si l'authentification a échoué, retourne une réponse avec un message d'erreur
        # et le code de statut HTTP 401
        # (Non autorisé).
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    #  création de requête complexe avec l'objet Q en combinant des expressions logiques
    # filtrer les objets de l'auteur OR les objets du contributeur
    def get_queryset(self):
        return Projects.objects.filter(
            Q(author_user_id=self.request.user.id) | Q(contributors__user_id=self.request.user.id)
        )

    # contributors__user_id fait référence à une relation "many-to-many"
    # entre les modèles Project et Contributor

    # Assigner un contributeur à un projet
    @action(detail=True, methods=['post'])
    def users(self, request, pk=None):
        project = self.get_object()
        serializer = ContributorsSerializer(data=request.data)
        if serializer.is_valid():
            contributor = serializer.save(project_id=project)
            contributor_data = ContributorsSerializer(contributor).data
            return Response(contributor_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Récupérer la liste des utilisateurs attachés à un projet
    @action(detail=True, methods=['get'])
    def get_users(self, request, pk=None):
        project = self.get_object()
        contributors = project.contributors.all()
        users = [contributor.user_id for contributor in contributors]
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class IssueViewSet(ModelViewSet):
    serializer_class = IssuesSerializer

    def get_queryset(self):
        return Issues.objects.all()


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorsSerializer
    http_method_names = ["get", "post"]

    def get_queryset(self):
        project_id = self.kwargs['project_pk']
        return Contributors.objects.filter(project_id=project_id)

    # filtrer les contributeurs en fonction de l'ID du projet,
    # qui est extrait de self.kwargs['project_pk']

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project_id = self.kwargs['project_pk']
        project = get_object_or_404(Projects, id=project_id)
        contributor = serializer.save(project_id=project)
        return Response(self.get_serializer(contributor).data, status=status.HTTP_201_CREATED)
    #  récupérer le projet correspondant à l'ID du projet transmis dans l'URL.
    #  J'ai utilisé get_object_or_404 pour récupérer l'objet Projects ou renvoyer une erreur 404
    #  si le projet n'existe pas. Ensuite, j'ai sauvegardé le contributeur en utilisant serializer
    #  .save(project_id=project) et renvoyé la réponse avec les données du contributeur créé.


class CommentViewSet(ModelViewSet):
    serializer_class = CommentsSerializer

    def get_queryset(self):
        return Comments.objects.all()


