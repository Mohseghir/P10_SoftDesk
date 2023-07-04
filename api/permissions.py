from rest_framework import permissions


class ProjectPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Autoriser uniquement les utilisateurs authentifiés à effectuer des opérations CRUD
        if request.method in permissions.SAFE_METHODS:
            return True  # Autoriser les opérations de lecture (GET)
        elif request.method == 'POST':
            return request.user.is_authenticated  # Autoriser la création (POST) uniquement pour les utilisateurs authentifiés
        else:
            return False  # Refuser les autres opérations (PUT, PATCH, DELETE)

    def has_object_permission(self, request, view, obj):
        # Autoriser les utilisateurs propriétaires à mettre à jour ou supprimer leur propre projet
        return request.user == obj.created_by
