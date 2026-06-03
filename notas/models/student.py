# notas/models/student.py
from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user              = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    enrollment_number = models.CharField(max_length=20, unique=True)
    date_of_birth     = models.DateField(null=True, blank=True)
    created_at        = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.enrollment_number})"