# notas/serializers/student.py
from rest_framework import serializers
from django.contrib.auth.models import User
from notas.models import Student

class StudentUserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class StudentSerializer(serializers.ModelSerializer):
    # Esto mostrará los datos del usuario en los GET, pero no afectará la escritura externa
    user_details = StudentUserSummarySerializer(source='user', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user', 'enrollment_number', 'date_of_birth', 'user_details', 'created_at']
        extra_kwargs = {
            'user': {'write_only': True}  # Para pasar solo el ID del usuario al crear el perfil
        }