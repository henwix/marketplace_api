from rest_framework.permissions import SAFE_METHODS, BasePermission


class SellerViewPermission(BasePermission):
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


class HasSellerProfilePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'seller_profile', None) is not None


class ReadOnlyOrHasSellerProfilePermission(HasSellerProfilePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return super().has_permission(request, view)
