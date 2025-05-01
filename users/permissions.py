from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.filter(isAdmin=True).exists()


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class IsUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj == request.user
