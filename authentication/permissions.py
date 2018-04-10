from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist
from .models import StudentModel

class AdminAccessPermission(permissions.BasePermission):
    """
    Checks whether the user is an admin
    """
    message='You are not an admin'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            student=StudentModel.objects.get(user=request.user)
            if student.is_admin:
                return True
        return False