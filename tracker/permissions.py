from rest_framework import permissions


class IsOwnerOrReadOnlyPublic(permissions.BasePermission):
    """
    Пользователь может делать полноценный CRUD только со своими привычками.
    Другие пользователи могут только читать публичные привычки.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.is_public or obj.creator == request.user
        return obj.creator == request.user
