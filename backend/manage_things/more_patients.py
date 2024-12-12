import os
import django

# Configurar o ambiente do Django antes de qualquer importação de modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MedSync.settings')
django.setup()

from django.contrib.auth.models import User
from patients.models import Patient
from faker import Faker
import random
import re

def create_patients():
    faker = Faker()

    for i in range(10):  # Altere o número de pacientes, se necessário
        cpf = ''.join([str(random.randint(0, 9)) for _ in range(11)])
        name = faker.name()
        birth_date = faker.date_of_birth(minimum_age=18, maximum_age=90)

        clean_name = re.sub(r'[^a-zA-Z0-9]', '', name.lower())  # Remove espaços e caracteres especiais
        email = f"{clean_name}@mail.com"

        # Criar o usuário associado
        user = User.objects.create_user(
            username=email,
            email=email,
            password='algo1234'
        )

        # Criar o paciente associado
        Patient.objects.create(
            user=user,
            name=name,
            cpf=cpf,
            birth_date=birth_date,
            status=False
        )

        print(f"Paciente criado: {name} - CPF: {cpf} - Username: {user.username}")


if __name__ == "__main__":
    create_patients()
