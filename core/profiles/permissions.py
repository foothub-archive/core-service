from rest_framework import permissions


class ProfilePermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True
        return request.user is not None

    def has_object_permission(self, request, view, obj):
        return request.method == 'GET' or request.user == obj
