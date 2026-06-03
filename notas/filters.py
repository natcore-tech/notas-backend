# notas/filters.py
import django_filters
from notas.models import Course, Enrollment, Grade

class CourseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model  = Course
        fields = ['is_active', 'credits']

class EnrollmentFilter(django_filters.FilterSet):
    # Permite buscar matrículas escribiendo parte del nombre del alumno
    student_name = django_filters.CharFilter(
        field_name='student__user__first_name', lookup_expr='icontains'
    )

    class Meta:
        model  = Enrollment
        fields = ['period', 'course', 'student']

class GradeFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    to_date   = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte')
    course    = django_filters.NumberFilter(field_name='enrollment__course__id')
    period    = django_filters.NumberFilter(field_name='enrollment__period__id')

    class Meta:
        model  = Grade
        fields = ['evaluation_type']