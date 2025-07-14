from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from .models import UserProfile, Task, Attendance, Types
from .serializers import UserProfileSerializer, TaskSerializer, AttendanceSerializer

class UserProfileView(APIView):
    """
    Handles CRUD operations for UserProfile model.
    Supports listing all profiles, retrieving a single profile, creating, updating, and deleting profiles.
    Only supervisors can create, update, or delete profiles.
    """
    permission_classes = [IsAuthenticated]  # Requires user to be authenticated for all methods

    def get_object(self, pk):
        """
        Helper method to retrieve a UserProfile by primary key.
        Args:
            pk (int): Primary key of the UserProfile.
        Returns:
            UserProfile or None if not found.
        """
        try:
            return UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            return None

    def get(self, request, pk=None):
        """
        Handles GET requests to list all profiles or retrieve a single profile.
        Args:
            request: HTTP request object.
            pk (int, optional): Primary key for single profile retrieval.
        Returns:
            Response with serialized data or error message.
        """
        if pk:
            # Retrieve single profile by pk
            profile = self.get_object(pk)
            if profile is None:
                return Response({'error': 'UserProfile not found.'}, status=status.HTTP_404_NOT_FOUND)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # List all profiles
            users = UserProfile.objects.all()
            serializer = UserProfileSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Handles POST requests to create a new UserProfile.
        Only supervisors can create profiles.
        Args:
            request: HTTP request object containing profile data.
        Returns:
            Response with created profile data or error message.
        """
        if request.user.role != Types.SUPERVISOR:
            return Response({'error': 'Only supervisors can create profiles.'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Handles PUT requests to update an existing UserProfile.
        Only supervisors can update profiles.
        Args:
            request: HTTP request object containing updated profile data.
            pk (int): Primary key of the profile to update.
        Returns:
            Response with updated profile data or error message.
        """
        profile = self.get_object(pk)
        if profile is None:
            return Response({'error': 'UserProfile not found.'}, status=status.HTTP_404_NOT_FOUND)
        if request.user.role != Types.SUPERVISOR:
            return Response({'error': 'Only supervisors can update profiles.'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Handles DELETE requests to remove a UserProfile.
        Only supervisors can delete profiles.
        Args:
            request: HTTP request object.
            pk (int): Primary key of the profile to delete.
        Returns:
            Response with success message or error message.
        """
        profile = self.get_object(pk)
        if profile is None:
            return Response({'error': 'UserProfile not found.'}, status=status.HTTP_404_NOT_FOUND)
        if request.user.role != Types.SUPERVISOR:
            return Response({'error': 'Only supervisors can delete profiles.'}, status=status.HTTP_401_UNAUTHORIZED)
        profile.delete()
        return Response({'message': 'UserProfile deleted.'}, status=status.HTTP_200_OK)

class TaskView(APIView):
    """
    Handles CRUD operations for Task model.
    Supports listing all tasks, retrieving a single task, creating, updating, and deleting tasks.
    Only supervisors can create or delete tasks; supervisors and assigned interns can update tasks.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper method to retrieve a Task by primary key.
        Args:
            pk (int): Primary key of the Task.
        Returns:
            Task or None if not found.
        """
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return None

    def get(self, request, pk=None):
        """
        Handles GET requests to list all tasks or retrieve a single task.
        Args:
            request: HTTP request object.
            pk (int, optional): Primary key for single task retrieval.
        Returns:
            Response with serialized data or error message.
        """
        if pk:
            task = self.get_object(pk)
            if task is None:
                return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            tasks = Task.objects.all()
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Handles POST requests to create a new Task.
        Only supervisors can create tasks.
        Args:
            request: HTTP request object containing task data.
        Returns:
            Response with created task data or error message.
        """
        if request.user.role != Types.SUPERVISOR:
            return Response({'error': 'Only supervisors can create tasks.'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Handles PUT requests to update an existing Task.
        Only supervisors or the assigned intern can update tasks.
        Args:
            request: HTTP request object containing updated task data.
            pk (int): Primary key of the task to update.
        Returns:
            Response with updated task data or error message.
        """
        task = self.get_object(pk)
        if task is None:
            return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
        if request.user.role != Types.SUPERVISOR and task.assigned_to != request.user:
            return Response({'error': 'Only supervisors or the assigned intern can update tasks.'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Handles DELETE requests to remove a Task.
        Only supervisors can delete tasks.
        Args:
            request: HTTP request object.
            pk (int): Primary key of the task to delete.
        Returns:
            Response with success message or error message.
        """
        task = self.get_object(pk)
        if task is None:
            return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
        if request.user.role != Types.SUPERVISOR:
            return Response({'error': 'Only supervisors can delete tasks.'}, status=status.HTTP_401_UNAUTHORIZED)
        task.delete()
        return Response({'message': 'Task deleted.'}, status=status.HTTP_200_OK)

class AttendanceView(APIView):
    """
    Handles CRUD operations for Attendance model.
    Supports listing all attendance records, retrieving a single record, creating, updating, and deleting records.
    Only supervisors can create or delete records; supervisors and the associated user can update records.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper method to retrieve an Attendance record by primary key.
        Args:
            pk (int): Primary key of the Attendance record.
        Returns:
            Attendance or None if not found.
        """
        try:
            return Attendance.objects.get(pk=pk)
        except Attendance.DoesNotExist:
            return None

    def get(self, request, pk=None):
        """
        Handles GET requests to list all attendance records or retrieve a single record.
        Args:
            request: HTTP request object.
            pk (int, optional): Primary key for single record retrieval.
        Returns:
            Response with serialized data or error message.
        """
        if pk:
            attendance = self.get_object(pk)
            if attendance is None:
                return Response({'error': 'Attendance record not found.'}, status=status.HTTP_404_NOT_FOUND)
            serializer = AttendanceSerializer(attendance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            attendances = Attendance.objects.all()
            serializer = AttendanceSerializer(attendances, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Handles POST requests to create a new Attendance record.
        Only supervisors can create attendance records.
        Args:
            request: HTTP request object containing attendance data.
        Returns:
            Response with created attendance data or error message.
        """
        if request.user.role != Types.SUPERVISOR:
            return Response({'error': 'Only supervisors can create attendance records.'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Handles PUT requests to update an existing Attendance record.
        Only supervisors or the associated user can update records.
        Args:
            request: HTTP request object containing updated attendance data.
            pk (int): Primary key of the record to update.
        Returns:
            Response with updated attendance data or error message.
        """
        attendance = self.get_object(pk)
        if attendance is None:
            return Response({'error': 'Attendance record not found.'}, status=status.HTTP_404_NOT_FOUND)
        if request.user.role != Types.SUPERVISOR and attendance.user != request.user:
            return Response({'error': 'Only supervisors or the user can update attendance.'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = AttendanceSerializer(attendance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Handles DELETE requests to remove an Attendance record.
        Only supervisors can delete attendance records.
        Args:
            request: HTTP request object.
            pk (int): Primary key of the record to delete.
        Returns:
            Response with success message or error message.
        """
        attendance = self.get_object(pk)
        if attendance is None:
            return Response({'error': 'Attendance record not found.'}, status=status.HTTP_404_NOT_FOUND)
        if request.user.role != Types.SUPERVISOR:
            return Response({'error': 'Only supervisors can delete attendance records.'}, status=status.HTTP_401_UNAUTHORIZED)
        attendance.delete()
        return Response({'message': 'Attendance record deleted.'}, status=status.HTTP_200_OK)

class AuthView(APIView):
    """
    Handles authentication operations: sign-in and sign-out.
    Uses an action parameter to determine the operation.
    """
    def post(self, request, action):
        """
        Handles POST requests for sign-in and sign-out operations.
        Args:
            request: HTTP request object.
            action (str): Either 'sign-in' or 'sign-out' to determine the operation.
        Returns:
            JsonResponse with success message, token (for sign-in), or error message.
        """
        if action == 'sign-in':
            # Authenticate user and generate token
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return JsonResponse({'message': 'Sign-in successful.', 'token': token.key}, status=status.HTTP_200_OK)
            return JsonResponse({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif action == 'sign-out':
            # Log out authenticated user
            if not request.user.is_authenticated:
                return JsonResponse({'message': 'No user signed in.'}, status=status.HTTP_401_UNAUTHORIZED)
            logout(request)
            return JsonResponse({'message': 'Sign-out successful.'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)

class MarkAttendanceView(APIView):
    """
    Allows interns to mark their own attendance.
    Creates a new Attendance record tied to the requesting user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handles POST requests to mark attendance for an intern.
        Only interns can mark their own attendance.
        Args:
            request: HTTP request object containing status (defaults to 'P').
        Returns:
            Response with created attendance data or error message.
        """
        if request.user.role != Types.INTERN:
            return Response({'error': 'Only interns can mark attendance.'}, status=status.HTTP_401_UNAUTHORIZED)
        data = {'user': request.user.id, 'status': request.data.get('status', 'P')}
        serializer = AttendanceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MarkTaskCompleteView(APIView):
    """
    Allows interns to mark their assigned tasks as complete.
    Updates the is_completed field of a Task.
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        """
        Handles PATCH requests to mark a task as complete.
        Only the assigned intern can mark the task as complete.
        Args:
            request: HTTP request object.
            pk (int): Primary key of the task to mark as complete.
        Returns:
            Response with success message or error message.
        """
        if request.user.role != Types.INTERN:
            return Response({'error': 'Only interns can mark tasks as complete.'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            task = Task.objects.get(pk=pk, assigned_to=request.user)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found or not assigned to you.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task, data={'is_completed': True}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Task marked as complete.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssignTaskView(APIView):
    """
    Allows supervisors to assign tasks to interns.
    Creates a new Task with the supervisor as the assigner.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handles POST requests to assign a new task.
        Only supervisors can assign tasks.
        Args:
            request: HTTP request object containing task data.
        Returns:
            Response with created task data or error message.
        """
        if request.user.role != Types.SUPERVISOR:
            return Response({'error': 'Only supervisors can assign tasks.'}, status=status.HTTP_401_UNAUTHORIZED)
        data = request.data.copy()
        data['assigned_by'] = request.user.id
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)