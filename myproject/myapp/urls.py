from django.urls import path
from rest_framework.authtoken import views as auth_views
from .views import (
    UserProfileView, TaskView, AttendanceView, AuthView,
    MarkAttendanceView, MarkTaskCompleteView, AssignTaskView
)

urlpatterns = [
    # UserProfile CRUD endpoints
    path('users/', UserProfileView.as_view(), name='user_list'),  # List all profiles or create a new profile
    path('users/<int:pk>/', UserProfileView.as_view(), name='user_detail'),  # Retrieve, update, or delete a profile by pk



    # Task CRUD endpoints
    path('tasks/', TaskView.as_view(), name='task_list'),  # List all tasks or create a new task
    path('tasks/<int:pk>/', TaskView.as_view(), name='task_detail'),  # Retrieve, update, or delete a task by pk



    # Attendance CRUD endpoints
    path('attendances/', AttendanceView.as_view(), name='attendance_list'),  # List all attendance records or create a new record
    path('attendances/<int:pk>/', AttendanceView.as_view(), name='attendance_detail'),  # Retrieve, update, or delete an attendance record by pk



    # Authentication endpoints
    path('sign-in/', AuthView.as_view(), {'action': 'sign-in'}, name='sign_in'),  # Handle user sign-in with token generation
    path('sign-out/', AuthView.as_view(), {'action': 'sign-out'}, name='sign_out'),  # Handle user sign-out



    # Specialized action endpoints
    path('attendances/mark/', MarkAttendanceView.as_view(), name='mark_attendance'),  # Interns mark their own attendance
    path('tasks/<int:pk>/complete/', MarkTaskCompleteView.as_view(), name='mark_task_complete'),  # Interns mark a task as complete
    path('tasks/assign/', AssignTaskView.as_view(), name='assign_task'),  # Supervisors assign tasks to interns



    # Token authentication endpoint
    path('api-token-auth/', auth_views.obtain_auth_token, name='api_token_auth'),  # Obtain auth token for API access
]