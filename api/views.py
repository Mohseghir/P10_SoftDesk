from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import Projects, Contributors, Issues, Comments
from api.serializers import ProjectSerializer, ContributorsSerializer, \
    LoginSerializer, RegisterSerializer, IssuesSerializer, CommentsSerializer


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


class LoginView(APIView):
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
            refresh = RefreshToken.for_user(user)

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

    def get_queryset(self):
        return Projects.objects.all()


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
