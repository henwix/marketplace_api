from rest_framework.permissions import BasePermission


class HasSellerProfilePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'seller_profile', None) is not None
