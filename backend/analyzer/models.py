from django.db import models

class Analysis(models.Model):
    prescription_id = models.IntegerField()
    content = models.TextField()  # resposta da IA
    tipo_risco = models.CharField(max_length=100, blank=True)  # novo campo para o tipo de risco
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Análise da Prescrição {self.prescription_id}"
