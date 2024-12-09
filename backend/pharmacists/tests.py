from django.test import TestCase
from django.contrib.auth.models import User
from backend.patients.models import Patient

class PatientTestSetup(TestCase):

    def setUp(self):
        # Criação de um usuário e paciente de teste
        user = User.objects.create_user(username='testcpf', email='test@example.com', password='testpassword')
        Patient.objects.create(
            user=user,
            name='Paciente Teste',
            cpf='12345678901',  # Certifique-se de usar um CPF válido para os validadores
            birth_date='2000-01-01',
            medic_info='Registro médico de teste',
            status=False  # Paciente não validado
        )

    def test_patient_creation(self):
        # Verifica se o paciente foi criado corretamente
        patient = Patient.objects.get(cpf='12345678901')
        self.assertEqual(patient.name, 'Paciente Teste')
        self.assertFalse(patient.status)  # Verifica se o paciente está não validado
        print("Paciente criado para teste: ", patient)
