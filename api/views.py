from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.generics import GenericAPIView
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

    def get_queryset(self):
        user = self.request.user
        return Projects.objects.filter(author_user_id=user)

    # affiché les projects en fonction du user connecté
    @action(detail=True, methods=['post'])
    def users(self, request, pk=None):
        project = self.get_object()
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            project.users.add(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # Exclure le champ project_id des données envoyées
        request.data.pop('project_id', None)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class IssueViewSet(ModelViewSet):
    serializer_class = IssuesSerializer

    def get_queryset(self):
        return Issues.objects.all()


class ContributorViewSet(ModelViewSet):
    serializer_class = ContributorsSerializer

    def get_queryset(self):
        return Contributors.objects.all()


class CommentViewSet(ModelViewSet):
    serializer_class = CommentsSerializer

    def get_queryset(self):
        return Comments.objects.all()
