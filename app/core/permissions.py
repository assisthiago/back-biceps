from rest_framework.permissions import BasePermission


class AllowAnyToCreate(BasePermission):
    """
    Custom permission to allow any user to create an object,
    but restricts other actions to authenticated users.
    """

    def has_permission(self, request, view):
        # Allow any user to create an object
        if request.method == "POST":
            return True
        # Allow authenticated users for other methods
        return request.user and request.user.is_authenticated
