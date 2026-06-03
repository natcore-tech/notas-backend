# notas/serializers/grade.py
from rest_framework import serializers
from notas.models import Grade

class GradeSerializer(serializers.ModelSerializer):
    student_name       = serializers.CharField(source='enrollment.student.user.get_full_name', read_only=True)
    course_name        = serializers.CharField(source='enrollment.course.name', read_only=True)
    evaluation_display = serializers.CharField(source='get_evaluation_type_display', read_only=True)

    class Meta:
        model = Grade
        fields = [
            'id', 'enrollment', 'evaluation_type', 'score', 
            'observations', 'student_name', 'course_name', 
            'evaluation_display', 'created_at', 'updated_at'
        ]

    def validate_score(self, value):
        # Valida que la calificación no sea negativa ni exceda el límite de 20.00 puntos
        if value < 0 or value > 20:
            raise serializers.ValidationError("La calificación debe estar estrictamente en el rango de 0.00 a 20.00.")
        return value

    def validate(self, attrs):
        enrollment      = attrs.get('enrollment')
        evaluation_type = attrs.get('evaluation_type')
        
        # Validamos duplicados considerando si es una creación nueva o una actualización
        request   = self.context.get('request')
        is_update = request and request.method in ['PUT', 'PATCH']
        
        qs = Grade.objects.filter(enrollment=enrollment, evaluation_type=evaluation_type)
        if is_update and self.instance:
            qs = qs.exclude(pk=self.instance.pk)
            
        if qs.exists():
            raise serializers.ValidationError(
                f"Ya existe una nota registrada para el tipo de evaluación '{evaluation_type}' en esta matrícula."
            )
        return attrs