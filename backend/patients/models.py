from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    cpf = models.CharField(
        max_length=11,
        unique=True,
        validators=[RegexValidator(regex=r'^\d{11}$', message='O CPF deve conter exatamente 11 dígitos')]
    )
    birth_date = models.DateField()
    prescriptions = models.ManyToManyField('prescriptions.Prescription', related_name='patient_prescriptions', blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} ({self.cpf})'
