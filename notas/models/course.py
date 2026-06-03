# notas/models/course.py
from django.db import models

class Course(models.Model):
    name        = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, default='')
    credits     = models.PositiveIntegerField(default=3)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name