# notas/views/enrollment.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from notas.models import Enrollment
from notas.serializers.enrollment import EnrollmentSerializer
from notas.pagination import StandardPagination

class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['period', 'course']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        # El personal ve todas las matrículas, el estudiante solo ve las de él
        if self.request.user.is_staff:
            return Enrollment.objects.select_related('student__user', 'course', 'period').all()
        return Enrollment.objects.select_related('student__user', 'course', 'period').filter(
            student__user=self.request.user
        )

    def check_permissions(self, request):
        super().check_permissions(request)
        # Deniega métodos de escritura (POST, PUT, PATCH, DELETE) si no es staff
        if request.method not in ['GET', 'HEAD', 'OPTIONS'] and not request.user.is_staff:
            self.permission_denied(request, message="No tienes autorización para modificar inscripciones.")