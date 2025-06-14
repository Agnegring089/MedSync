from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from pharmacists.permissions import pharmacist_required
from prescriptions.models import Prescription
from patients.models import Patient
from medicaments.models import Medicament  # <- integração
from django.utils.dateparse import parse_date
from django.contrib import messages
import json


@login_required
@pharmacist_required
def create_prescription(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        try:
            local_consultation = request.POST.get('local_consultation')
            crm = request.POST.get('crm')
            doctor_name = request.POST.get('doctor_name')

            date_input = request.POST.get('date')
            date = parse_date(date_input) if date_input else None

            medications_json = request.POST.get('medications')
            medications = json.loads(medications_json) if medications_json else []

            # Validação: impedir prescrição de medicamentos fora da base
            valid_names = set(Medicament.objects.values_list('nome', flat=True))
            invalids = [m['name'] for m in medications if m['name'] not in valid_names]

            if invalids:
                raise ValueError(f"Os seguintes medicamentos não estão cadastrados: {', '.join(invalids)}")

            # Criar nova prescrição
            Prescription.objects.create(
                patient=patient,
                local_consultation=local_consultation,
                crm=crm,
                doctor_name=doctor_name,
                date=date,
                medications=medications
            )

            return redirect('home_pharmaceutical')

        except Exception as e:
            return render(request, 'create_prescription.html', {
                'patient': patient,
                'medicaments': Medicament.objects.all(),
                'error': str(e)
            })

    return render(request, 'create_prescription.html', {
        'patient': patient,
        'medicaments': Medicament.objects.all()
    })


@login_required
@pharmacist_required
def view_prescriptions(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    prescriptions = Prescription.objects.filter(patient=patient).order_by('-date')

    prescriptions_with_medications = [
        {
            'prescription': prescription,
            'medications': prescription.medications
        }
        for prescription in prescriptions
    ]

    return render(request, 'view_prescriptions.html', {
        'patient': patient,
        'prescriptions_with_medications': prescriptions_with_medications,
    })


@login_required
@pharmacist_required
def delete_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)

    if request.method == 'POST':
        patient_id = prescription.patient.id
        prescription.delete()
        messages.success(request, "Prescrição excluída com sucesso.")
        return redirect('view_prescriptions', patient_id=patient_id)

    return render(request, 'confirm_delete_prescription.html', {
        'prescription': prescription
    })
