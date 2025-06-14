from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from pharmacists.permissions import pharmacist_required
from prescriptions.models import Prescription
from patients.models import Patient
from medicaments.models import Medicament
from analyzer.models import Analysis  # <- Importação do app analyzer
from django.utils.dateparse import parse_date
from django.contrib import messages
import json
import requests
from itertools import combinations


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

            valid_names = set(m.nome for m in Medicament.objects.all())
            invalids = [m['name'] for m in medications if m['name'] not in valid_names]
            if invalids:
                raise ValueError(f"Os seguintes medicamentos não estão cadastrados: {', '.join(invalids)}")

            # Criar a prescrição primeiro (sem analyze)
            prescription = Prescription.objects.create(
                patient=patient,
                local_consultation=local_consultation,
                crm=crm,
                doctor_name=doctor_name,
                date=date,
                medications=medications
            )

            # Analisar pares de medicamentos com IA
            pairs = list(combinations(medications, 2))
            analyze_result = []

            for pair in pairs:
                try:
                    response = requests.post(
                        'http://127.0.0.1:8000/analyzer/analyze_prescription/',
                        json={"medications": list(pair)}
                    )
                    if response.status_code == 200:
                        data = response.json()
                        analyze_result.append(
                            f"🧪 {pair[0]['name']} + {pair[1]['name']}: {data.get('recommendations', 'Sem recomendação.')}"
                        )
                        # Salvar análise individual no banco
                        Analysis.objects.create(
                            prescription_id=prescription.id,
                            content=data.get('recommendations', ''),
                            tipo_risco=data.get('tipo_risco', '')
                        )
                    else:
                        analyze_result.append(f"{pair[0]['name']} + {pair[1]['name']}: Falha na análise.")
                except Exception as e:
                    analyze_result.append(f"{pair[0]['name']} + {pair[1]['name']}: Erro - {str(e)}")

            # Atualizar o campo analyze do modelo Prescription com texto resumido
            prescription.analyze = "\n".join(analyze_result)
            prescription.save()

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

    prescriptions_with_medications = []
    for prescription in prescriptions:
        analysis = Analysis.objects.filter(prescription_id=prescription.id).first()
        prescriptions_with_medications.append({
            'prescription': prescription,
            'medications': prescription.medications,
            'analysis': analysis  # usado no template
        })

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
