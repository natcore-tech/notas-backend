# notas/models/period.py
from django.db import models

class AcademicPeriod(models.Model):
    name       = models.CharField(max_length=50, unique=True) # Ej: "Semestre 2026-A"
    start_date = models.DateField()
    end_date   = models.DateField()
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Academic Period'
        verbose_name_plural = 'Academic Periods'
        ordering            = ['-start_date']

    def __str__(self):
        return self.name