from rest_framework.permissions import BasePermission
from django.core.exceptions import ObjectDoesNotExist
from api import models


# Fonction pour vérifier si l'utilisateur est l'auteur d'un projet
def is_author(pk, user):
    try:
        content = models.Projects.objects.get(pk=pk)
        return content.author == user
    except ObjectDoesNotExist:
        return True


# Fonction pour vérifier si l'utilisateur est un contributeur d'un projet
def is_contributor(user, project):
    try:
        models.Contributors.objects.get(user=user, project=project)
        return True
    except ObjectDoesNotExist:
        return False


# Fonction pour vérifier si l'utilisateur est l'auteur d'un commentaire
def is_author_comment(pk, user):
    try:
        content = models.Comments.objects.get(pk=pk)
        return content.author_user_id == user
    except ObjectDoesNotExist:
        return True


# Les commentaires doivent être visibles par tous les contributeurs au
# projet et par le responsable du projet, mais seul leur auteur peut les
# actualiser ou les supprimer.
"""class IsContributorOrAuthorProjectInComments(BasePermission):
    def has_permission(self, request, view):
        if view.action in ("update", "destroy"):
            return is_author_comment(view.kwargs["pk"], request.user)
        return is_contributor(request.user,
                              view.kwargs["pk"]) or is_author(
            view.kwargs["pk"], request.user
        )"""

# Un problème ne peut être actualisé ou supprimé que par son auteur,
# mais il doit rester visible par tous les contributeurs au projet.

"""class IsContributorOrAuthorInProjects(BasePermission):
    def has_permission(self, request, view):
        if view.kwargs.get("pk") is None:
            return True
        if view.action == "create":
            return True
        if view.action in ("update", "destroy"):
            return is_author(view.kwargs["pk"], request.user)
        return is_contributor(request.user,
                              view.kwargs["pk"]) or is_author(
            view.kwargs["pk"], request.user
        )
"""

# Il est interdit à tout utilisateur autre que l'auteur de demander une mise à
# jour et de supprimer des demandes sur une question/un projet/un
# commentaire.

"""class IsContributorOrAuthor(BasePermission):
    def has_permission(self, request, view):
        if view.action in ("update", "destroy"):
            return is_author(request.user, view.kwargs["project_pk"])
        return is_contributor(view.kwargs["project_pk"], request.user)
"""


class IsContributorOrAuthorProjectInProjectView(BasePermission):
    def has_permission(self, request, view):
        if view.kwargs.get("pk") is None:
            return True
        if view.action == "create":
            return True
        if view.action in ("destroy", "update"):
            return is_author(view.kwargs["pk"], request.user)
        return is_contributor(request.user,
                              view.kwargs["pk"]) or is_author(
            view.kwargs["pk"], request.user
        )


class IsContributorOrAuthorProjectInContributorView(BasePermission):
    def has_permission(self, request, view):
        if view.action in ("create", "destroy", "update"):
            return is_author(view.kwargs["project_pk"], request.user)
        return is_contributor(
            request.user, view.kwargs["project_pk"]
        ) or is_author(view.kwargs["project_pk"], request.user)


class IsContributorOrAuthorProjectInIssueView(BasePermission):
    def has_permission(self, request, view):
        if view.action in ("destroy", "update"):
            return is_author(view.kwargs["project_pk"], request.user)
        return is_contributor(request.user, view.kwargs["project_pk"])


class IsContributorOrAuthorProjectInCommentView(BasePermission):
    def has_permission(self, request, view):
        if view.action in ("update", "destroy"):
            return is_author_comment(view.kwargs["pk"], request.user)
        return is_contributor(
            request.user, view.kwargs["project_pk"]
        ) or is_author(view.kwargs["project_pk"], request.user)
