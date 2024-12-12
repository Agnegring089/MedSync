# farmaceuticos/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Pharmaceutical

class PharmaceuticalRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirme a Senha')

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']
        labels = {
            'email': 'Email',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error('confirm_password', 'As senhas não correspondem.')

class PharmaceuticalForm(forms.ModelForm):
    class Meta:
        model = Pharmaceutical
        fields = ['name', 'crf']
        labels = {
            'name': 'Nome',
            'crf': 'CRF',
        }

class PharmaceuticalLoginForm(forms.Form):
    crf = forms.CharField(max_length=5, label='CRF')
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')
