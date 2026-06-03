# notas/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_staff)

class IsStudentOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Los profesores/administradores siempre tienen acceso
        if request.user.is_staff:
            return True
        
        # Si el objeto es el modelo Student
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # Si el objeto es una Enrollment (Matrícula)
        elif hasattr(obj, 'student'):
            return obj.student.user == request.user
        
        # Si el objeto es un Grade (Calificación)
        elif hasattr(obj, 'enrollment'):
            return obj.enrollment.student.user == request.user
            
        return False