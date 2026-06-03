# notas/models/enrollment.py
from django.db import models
from .student import Student
from .course import Course
from .period import AcademicPeriod

class Enrollment(models.Model):
    student    = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course     = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='enrollments')
    period     = models.ForeignKey(AcademicPeriod, on_delete=models.PROTECT, related_name='enrollments')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course', 'period') # Evita matrícula doble en la misma materia y periodo
        ordering        = ['-created_at']

    def __str__(self):
        return f"{self.student.user.username} - {self.course.name} ({self.period.name})"