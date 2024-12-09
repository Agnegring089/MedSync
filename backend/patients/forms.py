from django import forms
from django.contrib.auth.models import User
from .models import Patient
from django.core.exceptions import ValidationError
from datetime import date

class PatientRegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o email',
        }),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite a senha',
        }),
        label='Senha'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme a senha',
        }),
        label='Confirmar Senha'
    )
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        }),
        input_formats=['%Y-%m-%d'],
        label='Data de Nascimento'
    )

    class Meta:
        model = Patient
        fields = ['name', 'cpf', 'birth_date']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome',
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o CPF',
            }),
        }

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')

        # Verifica se a data está no futuro
        if birth_date > date.today():
            raise ValidationError('A data de nascimento não pode ser no futuro.')

        return birth_date

    def clean(self):
        cleaned_data = super().clean()
        cpf = cleaned_data.get('cpf')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Verifica se o CPF já existe
        if Patient.objects.filter(cpf=cpf).exists():
            self.add_error('cpf', 'Este CPF já está em uso.')

        # Verifica se o email já existe
        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Este email já está em uso.')

        # Verifica se as senhas são iguais
        if password != confirm_password:
            self.add_error('confirm_password', 'As senhas não correspondem.')

        return cleaned_data

class PatientEditForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'cpf', 'birth_date', 'prescriptions']

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if Patient.objects.filter(cpf=cpf).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Já existe um paciente com este CPF registrado.')
        return cpf