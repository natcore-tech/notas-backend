# notas/serializers/enrollment.py
from rest_framework import serializers
from notas.models import Enrollment

class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    course_name  = serializers.CharField(source='course.name', read_only=True)
    period_name  = serializers.CharField(source='period.name', read_only=True)

    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'course', 'period', 
            'student_name', 'course_name', 'period_name', 
            'created_at'
        ]

    def validate(self, attrs):
        student = attrs.get('student')
        course  = attrs.get('course')
        period  = attrs.get('period')
        
        # Validación explícita para evitar duplicados en la lógica del negocio
        if Enrollment.objects.filter(student=student, course=course, period=period).exists():
            raise serializers.ValidationError(
                "Este estudiante ya se encuentra matriculado en esta materia durante el periodo seleccionado."
            )
        return attrs