from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        elif view.action in ['create', 'retrieve', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated or request.user.is_superuser
        else:
            return False
