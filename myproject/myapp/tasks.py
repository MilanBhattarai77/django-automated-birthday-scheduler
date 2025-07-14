from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import UserProfile
from decouple import config

@shared_task
def send_happy_birthday_emails():
    """
    Sends Happy Birthday emails to users whose birth date matches the current day and month.
    Runs daily via Celery Beat to check for birthdays.
    """
    # Get today's date using Django's timezone-aware datetime
    today = timezone.now().date()
    # Filter active users whose birth date matches today's day and month
    users_with_birthday = UserProfile.objects.filter(
        birth_date__day=today.day,
        birth_date__month=today.month,
        is_active=True
    )

    for user in users_with_birthday:
        # Define email subject and personalized message
        subject = "Happy Birthday!"
        message = f"Dear {user.username},\n\nWishing you a very Happy Birthday from the team! Have a fantastic day!\n\nBest regards,\nYour App Team"
        # Send email using Django's send_mail function
        send_mail(
            subject=subject,
            message=message,
            from_email=config('EMAIL_HOST_USER'),  # Email sender from environment variable
            recipient_list=[user.email],  # User's email address
            fail_silently=False,  # Raise exception if email sending fails
        )

@shared_task
def send_good_morning_emails():
    """
    Sends Good Morning emails to all active users.
    Runs daily via Celery Beat to greet users.
    """
    # Retrieve all active users
    users = UserProfile.objects.filter(is_active=True)
    for user in users:
        # Define email subject and personalized message
        subject = "Good Morning!"
        message = f"Good Morning, {user.username}!\n\nWe hope you have a great day ahead!\n\nBest regards,\nYour App Team"
        # Send email using Django's send_mail function
        send_mail(
            subject=subject,
            message=message,
            from_email=config('EMAIL_HOST_USER'),  # Email sender from environment variable
            recipient_list=[user.email],  # User's email address
            fail_silently=False,  # Raise exception if email sending fails
        )