# notas/models/__init__.py
from .period import AcademicPeriod
from .course import Course
from .student import Student
from .enrollment import Enrollment
from .grade import Grade

# Mantienes el de user si creaste algo personalizado, 
# pero la autenticación base la sigue manejando django.contrib.auth.models.User