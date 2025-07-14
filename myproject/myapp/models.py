from django.db import models
from django.contrib.auth.models import AbstractUser



class Types(models.TextChoices):
    SUPERVISOR = "Supervisor", "Supervisor"
    INTERN = "Intern", "Intern"


class UserProfile(AbstractUser):
    role = models.CharField(max_length=20, choices=Types.choices, default=Types.INTERN)
    email = models.EmailField(unique=True, max_length=50)
    username = models.CharField(unique=True, max_length=20)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "role"]

    def __str__(self):
        return self.email




class Task(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="assigned_tasks", null=True, blank=True)
    assigned_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, related_name="assigned_by_tasks", null=True, blank=True)
    birth_date = models.DateField(help_text="User's date of birth", null=True, blank=True)

    def __str__(self):
        return self.title




class Attendance(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="attendances")
    status = models.CharField(max_length=10, choices=[('P', 'Present'), ('A', 'Absent'), ('L', 'Late')], default='A')
    check_in_time = models.DateTimeField(auto_now_add=True)
    check_out_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.status}"