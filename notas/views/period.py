# notas/views/period.py
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from notas.models import AcademicPeriod
from notas.serializers.period import AcademicPeriodSerializer
from notas.permissions import IsStaffOrReadOnly
from notas.pagination import StandardPagination

class AcademicPeriodViewSet(viewsets.ModelViewSet):
    queryset = AcademicPeriod.objects.all()
    serializer_class = AcademicPeriodSerializer
    permission_classes = [IsStaffOrReadOnly] # Permiso heredado de tu código anterior
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['start_date', 'name']
    ordering = ['-start_date']