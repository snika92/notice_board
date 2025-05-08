from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name='admins').exists()


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj == request.user
