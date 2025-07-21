from datetime import timedelta
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Task
from django.utils.timezone import now


@shared_task
def send_email_task(subject, message, recipient_list):
    """
    A Celery task to send an email.
    """
    print("Sending email with subject:", subject)
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )


@shared_task
def send_duedate_task():
    print("Checking for tasks due soon...")
    tasks = Task.objects.filter(
        due_date__lte=now() + timedelta(days=1), status='Pending')
    for task in tasks:
        send_email_task.delay(
            subject=f"Task Due Soon: {task.title}",
            message=f"Task '{task.title}' is due soon.",
            recipient_list=[task.assignee.email]
        )


@shared_task
def sample_task():
    """
    A sample Celery task that can be scheduled.
    """
    print("Sample task executed.")
    # You can add any logic here that you want to run periodically
    # For example, you could check for tasks due soon or send reminders
    send_duedate_task.delay()
