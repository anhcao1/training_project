# tasks/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=['Admin', 'Manager']).exists()


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Staff').exists()

class IsManagerOrAdminOrOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            task_data = request.data.get('task', {})
            assignee_id = task_data.get('assignee', '')
            return assignee_id == request.user.id 
        return True 
    def has_object_permission(self, request, view, obj):
        print("aaaa", obj.assignee, request.user)
        if request.user.groups.filter(name__in=['Admin', 'Manager']).exists():
            return True
        print(obj.assignee, request.user)
        return obj.assignee == request.user
