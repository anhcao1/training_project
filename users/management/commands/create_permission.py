from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Create default user permissions and assign them to groups'

    def handle(self, *args, **kwargs):
        # Define groups and their permissions
        group_permissions = {
            'Admin': ['add_user', 'change_user', 'delete_user', 'view_user'],
            'Manager': ['change_ticket', 'view_ticket'],
            'Staff': ['view_own_ticket'],
        }

        for group_name, perms in group_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            for perm_codename in perms:
                try:
                    permission = Permission.objects.get(codename=perm_codename)
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f'Permission {perm_codename} does not exist.'
                    ))
            group.save()