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


class IsGroupMember(permissions.BasePermission):
    """
    Allow access only if the user is a member of the group.
    """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.members.all() or request.user.is_superuser


class IsTeacherRelatedByGroup(permissions.BasePermission):
    """
    Allow access only if the group belongs to the user
    """

    def has_permission(self, request, view):
        if request.user.role not in ['teacher', 'admin']:
            return False

        group = request.data.get('group')
        if not group:
            return False

        # Check if the user is part of that group
        return request.user.groups.filter(title=group).exists()


class IsTeacherOrAdminOrStudentReadOnly(permissions.BasePermission):
    """
    - Allow GET (retrieve) for students.
    - Allow all actions for teachers and admins.
    - Deny others.
    """

    def has_object_permission(self, request, view, obj):
        # Check if user belongs to the group of the lesson
        user_groups = request.user.groups.all()

        if obj.group not in user_groups:
            return False

        # Only teacher or admin can write (update/delete)
        return request.user.role in ['teacher', 'admin']


class IsTeacher(permissions.BasePermission):
    """
    Teachers can create tasks.
    Only the task creator can update/delete the task.
    Others (students or other teachers) can only view.
    """

    def has_permission(self, request, view):
        group_slug = view.kwargs.get('slug')
        return request.user.groups.filter(slug=group_slug).exists() and request.user.role == 'teacher'


class IsTeacherOrStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        group_slug = view.kwargs.get('slug')
        return request.user.groups.filter(slug=group_slug).exists()
