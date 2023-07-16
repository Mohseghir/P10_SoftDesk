from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from .models import Projects, Contributors, Issues, Comments


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
        )
        return user


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]

###############


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = ["id", "title", "description", "project_type", "author"]


class ContributorsSerializer(ModelSerializer):
    class Meta:
        model = Contributors
        fields = ["id", "user", "project", "role"]


class IssuesSerializer(ModelSerializer):

    class Meta:
        model = Issues
        fields = ["id", "title", "description", "tag",
                  "priority", "project", "status", "author",
                  "assigned_user"]


class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = ["id", "description", "author_user_id", "issue_id"]




