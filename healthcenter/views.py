from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import HealthCenter
import json

@csrf_exempt
def AddHealthCenter(request):
    if request.method == "POST":
        try:
            # Carrega os dados do corpo da requisição como JSON
            data = json.loads(request.body)
            nome = data.get("nome")  
            telefone = data.get("telefone")  
            usuario_id = data.get("usuario_id")

            # Validações
            if not nome:
                return JsonResponse({"error": "O nome é obrigatório"}, status=400)
            if not telefone:
                return JsonResponse({"error": "O telefone é obrigatório"}, status=400)
            if not usuario_id:
                return JsonResponse({"error": "Usuário não encontrado"}, status=400)
            
            # Cria o centro de saúde
            healthcenter = HealthCenter.objects.create(
                nome=nome,
                telefone=telefone
            )
            
            return JsonResponse({"success": "Centro de saúde cadastrado com sucesso"}, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Dados inválidos no corpo da requisição"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)