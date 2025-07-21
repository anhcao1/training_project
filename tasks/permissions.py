from rest_framework.permissions import BasePermission


ADMIN_GROUPS = ('Admin', 'Manager')


def is_admin_or_manager(user):
    return (
        user and
        user.is_authenticated and
        user.groups.filter(name__in=ADMIN_GROUPS).exists()
    )


class IsAdminOrManager(BasePermission):

    def has_permission(self, request, view):
        return is_admin_or_manager(request.user)


class IsManagerOrAdminOrOwner(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if is_admin_or_manager(user):
            print("")
            return True
        if not user or not user.is_authenticated:
            return False

        if request.method == 'POST':
            data = request.data or {}
            return (
                data.get('assignee') == user.id or
                data.get('owner') == user.id
            )
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if is_admin_or_manager(user):
            return True
        return (
            getattr(obj, 'assignee_id', None) == user.id or
            getattr(obj, 'owner_id', None) == user.id
        )
