from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    AUTH_REQUIRED_ACTION = [
        'update',
        'partial_update',
        'retrieve',
        'set_password',
        'destroy',
    ]
    AUTH_NOT_REQUIRED_ACTION = [
        'create',
    ]

    def has_permission(self, request, view):
        if view.action in self.AUTH_NOT_REQUIRED_ACTION:
            return True

        if view.action in self.AUTH_REQUIRED_ACTION and request.user.is_authenticated:
            return True

        return False
