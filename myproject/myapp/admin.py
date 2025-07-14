from django.contrib import admin
from .models import UserProfile
from .models import Task
from .models import Attendance

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Task)
admin.site.register(Attendance)
