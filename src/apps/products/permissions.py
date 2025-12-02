from rest_framework.permissions import BasePermission


class ProductPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and getattr(user, 'seller_profile', None) is not None

    def has_object_permission(self, request, view, obj):
        return obj.seller_id == request.user.seller_profile.id
