from rest_framework.permissions import BasePermission
from django.core.exceptions import ObjectDoesNotExist
from api import models


# Fonction pour vérifier si l'utilisateur est l'auteur d'un projet
def is_author(pk, user):
    try:
        content = models.Projects.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return True
    return content.author == user


# Fonction pour vérifier si l'utilisateur est un contributeur d'un projet
def is_contributor(user, project):
    try:
        models.Contributors.objects.get(user=user, project=project)
    except ObjectDoesNotExist:
        return False
    return True


# Fonction pour vérifier si l'utilisateur est l'auteur d'un commentaire
def is_author_comment(pk, user):
    try:
        content = models.Comments.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return True
    return content.author_user_id == user


# Permission pour vérifier si l'utilisateur est un contributeur ou l'auteur d'un projet
class IsContributorOrAuthorProjectPermission(BasePermission):
    def has_permission(self, request, view):
        project_pk = view.kwargs.get("project_pk")
        pk = view.kwargs.get("pk")

        if view.action in ("create", "destroy", "update"):
            return is_author(project_pk, request.user)

        return is_contributor(request.user, project_pk) or is_author(project_pk, request.user)


# Permission pour vérifier si l'utilisateur est l'auteur d'un commentaire
class IsAuthorCommentPermission(BasePermission):
    def has_permission(self, request, view):
        pk = view.kwargs.get("pk")

        if view.action == "update":
            return is_author_comment(pk, request.user)

        return True
