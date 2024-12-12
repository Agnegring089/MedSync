from logging import exception

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from pharmacists.permissions import pharmacist_required
from prescriptions.models import Prescription
from patients.models import Patient
from django.utils.dateparse import parse_date

@login_required
@pharmacist_required
def create_prescription(request, patient_id):
    # Buscar o paciente pelo ID
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        try:
            # Coletar os dados do formulário
            local_consultation = request.POST.get('local_consultation')
            crm = request.POST.get('crm')
            doctor_name = request.POST.get('doctor_name')
            date = parse_date(request.POST.get('date'))  # Convertendo a data para formato válido

            # Criar uma nova prescrição
            prescription = Prescription.objects.create(
                patient=patient,
                local_consultation=local_consultation,
                crm=crm,
                doctor_name=doctor_name,
                date=date,
                medications=[]  # Inicializa a lista vazia
            )

            # Adicionar medicamentos
            medication = {
                "name": request.POST.get('medication_name'),
                "dose": request.POST.get('dose'),
                "frequency": request.POST.get('frequency'),
                "duration_days": int(request.POST.get('duration_days')),
                "quantity": int(request.POST.get('quantity')),
                "medication_type": request.POST.get('medication_type')
            }
            prescription.medications.append(medication)
            prescription.save()

            # Redirecionar para a página inicial do farmacêutico
            return redirect('home_pharmaceutical')
        except Exception as e:
            print(exception)
            return render(request, 'create_prescription.html', {'patient': patient, 'error': str(e)})

    return render(request, 'create_prescription.html', {'patient': patient})

@login_required
@pharmacist_required
def view_prescriptions(request, patient_id):
    # Buscar o paciente e suas prescrições
    patient = get_object_or_404(Patient, id=patient_id)
    prescriptions = Prescription.objects.filter(patient=patient).order_by('-date')

    # Preparar os medicamentos para exibição
    prescriptions_with_medications = [
        {
            'prescription': prescription,
            'medications': prescription.medications  # A lista de medicamentos
        }
        for prescription in prescriptions
    ]

    return render(request, 'view_prescriptions.html', {
        'patient': patient,
        'prescriptions_with_medications': prescriptions_with_medications,
    })
