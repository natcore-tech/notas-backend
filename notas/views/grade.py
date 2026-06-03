# notas/views/grade.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Max, Min, Count

from notas.models import Grade
from notas.serializers.grade import GradeSerializer
from notas.pagination import StandardPagination

class GradeViewSet(viewsets.ModelViewSet):
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['evaluation_type', 'enrollment__course', 'enrollment__period']
    ordering_fields = ['score', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        # Profesores ven todo, alumnos únicamente su récord de calificaciones
        if self.request.user.is_staff:
            return Grade.objects.select_related('enrollment__student__user', 'enrollment__course').all()
        return Grade.objects.select_related('enrollment__student__user', 'enrollment__course').filter(
            enrollment__student__user=self.request.user
        )

    def check_permissions(self, request):
        super().check_permissions(request)
        # Los estudiantes solo tienen acceso de lectura (GET)
        if request.method not in ['GET', 'HEAD', 'OPTIONS'] and not request.user.is_staff:
            self.permission_denied(request, message="Solo los docentes pueden registrar o editar calificaciones.")

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        # Muestra métricas generales del rendimiento estudiantil (Solo profesores/admin)
        if not request.user.is_staff:
            return Response({'error': 'Acceso denegado.'}, status=status.HTTP_403_FORBIDDEN)
        
        qs = Grade.objects.all()
        data = qs.aggregate(
            total_grades=Count('id'),
            avg_score=Avg('score'),
            max_score=Max('score'),
            min_score=Min('score')
        )
        if data['avg_score']:
            data['avg_score'] = round(float(data['avg_score']), 2)
        return Response(data)