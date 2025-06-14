from django.db import models

class Medicament(models.Model):
    TIPO_CHOICES = [
        ('comprimido', 'Comprimido'),
        ('capsula', 'Cápsula'),
        ('injetavel', 'Injetável'),
    ]

    nome_convencional = models.CharField(max_length=100)
    dose = models.CharField(max_length=50)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    estoque = models.PositiveIntegerField(default=0)

    @property
    def nome(self):
        return f"{self.nome_convencional} {self.dose} ({self.get_tipo_display()})"

    def __str__(self):
        return self.nome
