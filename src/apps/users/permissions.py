from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    AUTH_REQUIRED_ACTIONS = [
        'update',
        'partial_update',
        'retrieve',
        'set_password',
        'destroy',
    ]
    AUTH_NOT_REQUIRED_ACTIONS = [
        'create',
    ]

    def has_permission(self, request, view):
        action = getattr(view, 'action', None)

        if action in self.AUTH_NOT_REQUIRED_ACTIONS:
            return True

        if action in self.AUTH_REQUIRED_ACTIONS and request.user.is_authenticated:
            return True

        return False
