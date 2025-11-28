from rest_framework.permissions import BasePermission


class SellerPermission(BasePermission):
    SELLER_PROFILE_REQUIRED = [
        'update',
        'partial_update',
        'retrieve',
        'destroy',
    ]
    SELLER_PROFILE_NOT_REQUIRED = [
        'create',
    ]

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        action = getattr(view, 'action', None)
        has_seller_profile = getattr(user, 'seller_profile', None) is not None

        if action in self.SELLER_PROFILE_NOT_REQUIRED and not has_seller_profile:
            return True

        if action in self.SELLER_PROFILE_REQUIRED and has_seller_profile:
            return True

        return False
