# notas/serializers/course.py
from rest_framework import serializers
from notas.models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'