from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Create default user groups'

    def handle(self, *args, **kwargs):
        print("Creating default user groups...")
        groups = ['Admin', 'Manager', 'Staff']
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                print(f"Group '{group_name}' created.")
            else:
                print(f"Group '{group_name}' already exists.")