from django.db import models
from patients.models import Patient

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_prescriptions')
    local_consultation = models.CharField(max_length=255)
    crm = models.CharField(max_length=20)
    doctor_name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    medications = models.JSONField(default=list)

    def __str__(self):
        return f"Prescrição para {self.patient.name} em {self.date}"

class Medication(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='medication_list')
    name = models.CharField(max_length=100)
    dose = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    duration_days = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)
    medication_type = models.CharField(
        max_length=20,
        choices=[
            ('capsule', 'Comprimido/Cápsula'),
            ('liquid', 'Líquido (Gotas/ml)'),
            ('injectable', 'Injetável'),
        ],
        default='capsule'
    )

    def __str__(self):
        return f"{self.name} ({self.dose})"
