from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Medicament

def list_and_create_medicaments(request):
    if request.method == 'POST':
        nome_convencional = request.POST.get('nome_convencional')
        dose = request.POST.get('dose')
        tipo = request.POST.get('tipo')
        estoque = request.POST.get('estoque')

        try:
            estoque = int(estoque)
            Medicament.objects.create(
                nome_convencional=nome_convencional,
                dose=dose,
                tipo=tipo,
                estoque=estoque
            )
            messages.success(request, 'Medicamento cadastrado com sucesso.')
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar medicamento: {e}')

        return redirect('medicament_list')

    medicaments = Medicament.objects.all().order_by('nome_convencional')
    return render(request, 'medicaments_list.html', {
        'medicaments': medicaments
    })

def edit_medicament(request, medicament_id):
    medicament = get_object_or_404(Medicament, id=medicament_id)

    if request.method == 'POST':
        medicament.nome_convencional = request.POST.get('nome_convencional')
        medicament.dose = request.POST.get('dose')
        medicament.tipo = request.POST.get('tipo')
        try:
            medicament.estoque = int(request.POST.get('estoque'))
            medicament.save()
            messages.success(request, 'Medicamento atualizado com sucesso.')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar: {e}')

    return redirect('medicament_list')


def delete_medicament(request, medicament_id):
    medicament = get_object_or_404(Medicament, id=medicament_id)

    if request.method == 'POST':
        medicament.delete()
        messages.success(request, 'Medicamento excluído com sucesso.')

    return redirect('medicament_list')