# notas/views/student.py
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from notas.models import Student
from notas.serializers.student import StudentSerializer
from notas.pagination import StandardPagination

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('user').all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser] # Solo los administradores gestionan los perfiles de estudiantes directamente
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['enrollment_number', 'user__username', 'user__first_name', 'user__last_name']
    ordering_fields = ['enrollment_number', 'created_at']
    ordering = ['enrollment_number']