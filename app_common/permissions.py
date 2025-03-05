from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    from rest_framework import permissions
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj) -> bool:
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.username == request.user


class IsSuperAdmin(permissions.BasePermission):
    """
    Custom permission to grant access only to superusers or users in the 'SuperAdmins' group.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
                request.user.is_superuser
        )
