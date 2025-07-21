from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Task 
from .tasks import send_email_task


@receiver(pre_save, sender=Task)
def detect_status_change(sender, instance, **kwargs):
    if instance.pk:
        old_task = Task.objects.get(pk=instance.pk)
        instance._status_changed = old_task.status != instance.status
    else:
        instance._status_changed = False


@receiver(post_save, sender=Task)
def send_email_on_task_creation_or_update(sender, instance, created, **kwargs):
    if created:
        send_email_task.delay(
            subject=f"New Task Created: {instance.title}",
            message=(
                f"Task '{instance.title}' has been created with status "
                f"'{instance.status}'."
            ),
            recipient_list=[instance.assignee.email]
        )
    elif instance._status_changed:
        send_email_task.delay(
            subject=f"Task Updated: {instance.title}",
            message=(
                f"Task '{instance.title}' has been updated to status "
                f"'{instance.status}'."
            ),
            recipient_list=[instance.assignee.email]
        )
