from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, \
    SerializerMethodField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Projects, Contributors, Issues, Comments


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"]
        )
        return user


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]


class LoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]


###############


class ProjectSerializer(ModelSerializer):
    # creation de l'instance des issues qui est reliée aux projects comme dans le cours
    issues = SerializerMethodField()

    class Meta:
        model = Projects
        fields = ("id", "title", "description", "type", "author_user_id", "issues")

    def get_issues(self, instance):
        queryset = Issues.objects.filter(project_id=instance)
        serializer = IssuesSerializer(queryset, many=True)
        return serializer.data

    def get_queryset(self):
        user = self.request.user
        return Projects.objects.filter(contributors__user_id=user)
    # contributors__user_id fait référence à une relation "many-to-many"
    # entre les modèles Project et Contributor

class IssuesSerializer(ModelSerializer):
    # creation de l'instance de comments qui est reliée aux issues comme dans le cours
    comments = SerializerMethodField()

    class Meta:
        model = Issues
        fields = ("title", "desc", "issue_id", "tag",
                  "priority", "project_id", "status", "author_user_id",
                  "assignee_user_id", "created_time", "comments")

    def get_comments(self, instance):
        queryset = Comments.objects.filter(issue_id=instance)
        serializer = CommentsSerializer(queryset, many=True)
        return serializer.data


class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = ["comment_id", "description",
                  "author_user_id", "issue_id", "created_time"]
        read_only_fields = ["comment_id", "author_id", "issue_id"]


class ContributorsSerializer(ModelSerializer):
    user = SerializerMethodField()

    class Meta:
        model = Contributors
        fields = ["id", "user_id", "role", "user"]

    def get_user(self, instance):
        queryset = User.objects.get(id=instance.user_id.id)
        serializer = UserSerializer(queryset, many=False)
        return serializer.data
