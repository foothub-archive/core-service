from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    """
    Use this class to check if a user is authenticated instead of
    rest_framework's one.
    (because our "User" model does not implement the "is_authenticated" method)
    """

    def has_permission(self, request, view):
        return request.user is not None
