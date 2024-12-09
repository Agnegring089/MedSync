from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .models import Patient
from django.db import IntegrityError
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class PatientRegisterView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('name')
        cpf = request.data.get('cpf')
        birth_date = request.data.get('birth_date')

        try:
            # Verifica se já existe um paciente com o mesmo CPF
            if Patient.objects.filter(cpf=cpf).exists():
                return Response({'error': 'Já existe um paciente cadastrado com este CPF.'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Verifica se já existe um usuário com o mesmo email
            if User.objects.filter(email=email).exists():
                return Response({'error': 'Já existe um usuário cadastrado com este email.'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Criar o usuário associado (username será o email)
            user = User.objects.create_user(username=email, email=email, password=password)

            # Criar o paciente com status padrão como False
            Patient.objects.create(
                user=user,
                name=name,
                cpf=cpf,
                birth_date=birth_date,
                status=False  # Status padrão
            )

            return Response({'message': 'Cadastro realizado com sucesso!'}, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            if 'UNIQUE constraint' in str(e):  # Tratamento de duplicação
                return Response({'error': 'Erro de duplicação de dados.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'Erro ao processar a solicitação.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PatientLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Autentica o usuário
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                # Verifica se o usuário está vinculado a um paciente
                patient = Patient.objects.get(user=user)

                # Verifica se o status do paciente permite login
                if not patient.status:
                    return Response({'error': 'Conta do paciente está inativa'}, status=403)

                # Gera tokens JWT
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'patient_name': patient.name,
                    'status': patient.status,
                })
            except Patient.DoesNotExist:
                return Response({'error': 'Usuário não é um paciente'}, status=403)

        # Credenciais inválidas
        return Response({'error': 'Usuário ou senha incorretos'}, status=401)


class PatientDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Log dos cabeçalhos para depuração
        print("Cabeçalhos recebidos:", request.headers.get('Authorization'))

        try:
            # Buscar o paciente associado ao usuário autenticado
            patient = Patient.objects.get(user=request.user)
            return Response({
                'name': patient.name,
                'cpf': patient.cpf,
                'birth_date': patient.birth_date,
                'status': patient.status,
            })
        except Patient.DoesNotExist:
            # Retorna erro se o usuário autenticado não for um paciente
            return Response({'error': 'Usuário autenticado não é um paciente.'}, status=404)
