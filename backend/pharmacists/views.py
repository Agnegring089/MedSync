# farmaceuticos/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PharmaceuticalRegistrationForm, PharmaceuticalForm, PharmaceuticalLoginForm
from patients.models import Patient
from patients.forms import PatientRegistrationForm, PatientEditForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404

def register_pharmaceutical(request):
    if request.method == 'POST':
        user_form = PharmaceuticalRegistrationForm(request.POST)
        pharmaceutical_form = PharmaceuticalForm(request.POST)
        if user_form.is_valid() and pharmaceutical_form.is_valid():
            # Criar o usuário
            user = user_form.save(commit=False)
            user.username = user_form.cleaned_data['email']  # Usar o email como username
            user.set_password(user_form.cleaned_data['password'])
            user.is_active = True  # Defina conforme necessário
            user.save()
            # Criar o perfil do farmacêutico
            pharmaceutical = pharmaceutical_form.save(commit=False)
            pharmaceutical.user = user
            pharmaceutical.save()
            messages.success(request, 'Cadastro realizado com sucesso! Aguarde a aprovação do administrador.')
            return redirect('login_pharmaceutical')
    else:
        user_form = PharmaceuticalRegistrationForm()
        pharmaceutical_form = PharmaceuticalForm()
    return render(request, '../templates/register_pharmaceutical.html', {
        'user_form': user_form,
        'pharmaceutical_form': pharmaceutical_form
    })

def login_pharmaceutical(request):
    if request.method == 'POST':
        form = PharmaceuticalLoginForm(request.POST)
        if form.is_valid():
            crf = form.cleaned_data['crf']
            password = form.cleaned_data['password']
            user = authenticate(request, username=crf, password=password)
            if user is not None:
                if hasattr(user, 'pharmaceutical'):
                    if user.pharmaceutical.status:
                        login(request, user)
                        return redirect('home_pharmaceutical')  # Ajuste para a URL correta
                    else:
                        messages.error(request, 'Sua conta ainda não foi aprovada pelo administrador.')
                else:
                    messages.error(request, 'Credenciais inválidas.')
            else:
                messages.error(request, 'Credenciais inválidas.')
    else:
        form = PharmaceuticalLoginForm()
    return render(request, '../templates/login_pharmaceutical.html', {'form': form})

@login_required
def logout_pharmaceutical(request):
    logout(request)
    return redirect('login_pharmaceutical')  # Redireciona para a página de login

@login_required
def home_pharmaceutical(request):
    if not hasattr(request.user, 'pharmaceutical'):
        return redirect('login_pharmaceutical')

    query = request.GET.get('search', '')  # Obtém o termo de busca da barra de pesquisa
    if query:
        patients = Patient.objects.filter(
            Q(name__icontains=query) | Q(cpf__icontains=query)
        )
    else:
        patients = Patient.objects.all()

    pending_patients = Patient.objects.filter(status=False)
    recent_patients = Patient.objects.filter(status=True).order_by('-id')[:10]

    context = {
        'patients': patients,
        'search_query': query,
        'pending_patients': pending_patients,
        'recent_patients': recent_patients,
    }
    return render(request, '../templates/home_pharmaceutical.html', context)

@login_required
def register_patient(request):
    if not hasattr(request.user, 'pharmaceutical'):
        return redirect('login_pharmaceutical')

    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            # Criação do paciente
            patient = form.save(commit=False)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=patient.cpf, email=email, password=password)
            patient.user = user
            patient.status = True  # Paciente aprovado automaticamente
            patient.save()

            # Mensagem de sucesso
            messages.success(request, 'Paciente cadastrado com sucesso!')
            return redirect('home_pharmaceutical')  # Redireciona para a página inicial

    else:
        form = PatientRegistrationForm()

    return render(request, '../templates/register_patient.html', {'form': form})

@login_required
def approve_patient(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    patient.status = True  # Marca o paciente como aprovado
    patient.save()
    messages.success(request, f'Paciente {patient.name} aprovado com sucesso!')
    return redirect('home_pharmaceutical')

@login_required
def deny_patient(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    patient.delete()  # Exclui o paciente
    messages.success(request, f'Paciente {patient.name} foi negado.')
    return redirect('home_pharmaceutical')

@login_required
def view_patient(request, patient_id):
    if not hasattr(request.user, 'pharmaceutical'):
        return redirect('login_pharmaceutical')

    # Busca o paciente pelo ID ou retorna 404 se não encontrado
    patient = get_object_or_404(Patient, id=patient_id)

    # Renderiza a página de visualização com os detalhes do paciente
    return render(request, '../templates/view_patient.html', {'patient': patient})

@login_required
def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = PatientEditForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente atualizado com sucesso!')
            return redirect('home_pharmaceutical')
    else:
        form = PatientEditForm(instance=patient)

    return render(request, '../templates/edit_patient.html', {'form': form, 'patient': patient})

@login_required
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        patient.delete()
        messages.success(request, f'Paciente {patient.name} foi excluído com sucesso.')
        return redirect('home_pharmaceutical')
    return render(request, '../templates/confirm_delete.html', {'patient': patient})