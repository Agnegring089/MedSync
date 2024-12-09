import os
import django

# Configurar o ambiente do Django antes de acessar os modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MedSync.settings')  # Substitua 'MedSync.settings' pelo nome correto
django.setup()

from patients.models import Patient  # Certifique-se de que o caminho para o modelo está correto

def delete_all_patients():
    try:
        # Contar o número de pacientes antes de apagar
        total_patients = Patient.objects.count()
        if total_patients == 0:
            print("Nenhum paciente encontrado para apagar.")
            return

        # Apagar todos os pacientes
        Patient.objects.all().delete()
        print(f"Todos os {total_patients} pacientes foram apagados com sucesso.")
    except Exception as e:
        print("Erro ao apagar pacientes:", e)
