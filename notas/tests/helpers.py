# notas/tests/helpers.py
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date

from notas.models import AcademicPeriod, Course, Student, Enrollment, Grade

def create_user(username='user', email=None, password='Pass1234!', **kwargs):
    email = email or f'{username}@test.com'
    return User.objects.create_user(
        username=username, email=email, password=password, **kwargs
    )

def create_staff(username='staff', email=None, password='Admin1234!'):
    email = email or f'{username}@test.com'
    return User.objects.create_user(
        username=username, email=email, password=password, is_staff=True
    )

def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token), str(refresh)

def auth_client(user):
    client = APIClient()
    access, _ = get_tokens(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
    return client

def create_period(name='2026-A', is_active=True):
    return AcademicPeriod.objects.create(
        name=name, start_date=date(2026, 4, 1), end_date=date(2026, 8, 31), is_active=is_active
    )

def create_course(name='Bases de Datos', credits=4, is_active=True):
    return Course.objects.create(name=name, credits=credits, is_active=is_active)

def create_student(user, enrollment_number='UTE-001'):
    return Student.objects.create(user=user, enrollment_number=enrollment_number)

def create_enrollment(student, course, period):
    return Enrollment.objects.create(student=student, course=course, period=period)

def create_grade(enrollment, evaluation_type='parcial_1', score=18.50):
    return Grade.objects.create(
        enrollment=enrollment, evaluation_type=evaluation_type, score=score
    )