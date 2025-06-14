from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

@csrf_exempt
def analyze_prescription(request):
    if request.method == 'POST':
        try:
            print("🔍 Recebendo requisição...")

            data = json.loads(request.body)
            print("📦 Dados recebidos:", data)

            medications = data.get('medications', [])
            if not medications:
                return JsonResponse({'error': 'Nenhum medicamento fornecido.'}, status=400)

            # Construção do prompt
            prompt = (
                "Analise a combinação dos seguintes medicamentos, considerando interações medicamentosas e "
                "melhores horários para administração. Informe também o nível de risco (baixo, moderado ou alto). "
                "Formato: recomendação + campo 'Risco: <nível>'.\n\n"
            )
            for med in medications:
                prompt += f"- {med['name']} {med.get('dose', '')} {med.get('frequency', '')}\n"

            # Nova chamada à API com OpenAI >= 1.0.0
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Você é um farmacêutico especialista em interações medicamentosas."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=500
            )

            result = response.choices[0].message.content.strip()
            print("🤖 Resposta da IA:", result)

            # Extração do risco
            risk_level = "não identificado"
            for line in result.lower().splitlines():
                if "risco" in line:
                    if "alto" in line:
                        risk_level = "alto"
                    elif "moderado" in line:
                        risk_level = "moderado"
                    elif "baixo" in line:
                        risk_level = "baixo"
                    break

            return JsonResponse({
                "recommendations": result,
                "tipo_risco": risk_level
            })

        except Exception as e:
            print("❌ Erro na análise:", str(e))
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'message': 'Método não permitido'}, status=405)
