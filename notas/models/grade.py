# notas/models/grade.py
from django.db import models
from .enrollment import Enrollment

class Grade(models.Model):
    EVALUATION_CHOICES = [
        ('parcial_1', 'Parcial 1'),
        ('parcial_2', 'Parcial 2'),
        ('examen_final', 'Examen Final'),
        ('supletorio', 'Supletorio'),
    ]

    enrollment      = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='grades')
    evaluation_type = models.CharField(max_length=20, choices=EVALUATION_CHOICES)
    score           = models.DecimalField(max_digits=5, decimal_places=2) # Soporta notas como 18.50 o 100.00
    observations    = models.TextField(blank=True, default='')
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('enrollment', 'evaluation_type') # Una nota por tipo de evaluación
        ordering        = ['-created_at']

    def __str__(self):
        return f"{self.enrollment} | {self.get_evaluation_type_display()}: {self.score}"