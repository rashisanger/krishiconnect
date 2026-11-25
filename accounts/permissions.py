
from rest_framework.permissions import BasePermission


class IsFarmer(BasePermission):
    """
    Allows access only to authenticated farmer users.
    """

    message = "Only farmers can access this resource."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'FARMER'
        )


class IsBuyer(BasePermission):
    """
    Allows access only to authenticated buyer users.
    """

    message = "Only buyers can access this resource."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'BUYER'
        )


class IsAdmin(BasePermission):
    """
    Allows access only to authenticated admin users.
    """

    message = "Only administrators can access this resource."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'ADMIN'
        )
