
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Pharmaceutical(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pharmaceutical')
    name = models.CharField(max_length=255)
    crf = models.CharField(
        max_length=5,
        unique=True,
        validators=[RegexValidator(regex=r'^\d{5}$', message='O CRF deve conter exatamente 5 dígitos')]
    )
    status = models.BooleanField(default=False)  # Indica se o farmacêutico está aprovado

    def __str__(self):
        return f'{self.name} ({self.user.email})'
