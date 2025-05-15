from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import HealthCenter
import json

@csrf_exempt
def AddHealthCenter(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            nome = data.get("nome")  
            telefone = data.get("telefone")  
            usuario_id = data.get("usuario_id")
            if not nome:
                return JsonResponse({"error": "O nome é obrigatório"}, status=400)
            if not telefone:
                return JsonResponse({"error": "O telefone é obrigatório"}, status=400)
            if not usuario_id:
                return JsonResponse({"error": "Usuário não encontrado"}, status=400)
            from users.models import User
            try:
                usuario = User.objects.get(id=usuario_id)
            except User.DoesNotExist:
                return JsonResponse({"error": "Usuário não encontrado"}, status=404)
            healthcenter = HealthCenter.objects.create(
                nome=nome,
                telefone=telefone,
                usuario=usuario  
            )
            return JsonResponse({"success": "Centro de saúde cadastrado com sucesso"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Dados inválidos no corpo da requisição"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            nome = data.get("nome")  
            telefone = data.get("telefone")  
            usuario_id = data.get("usuario_id")

            
            if not nome:
                return JsonResponse({"error": "O nome é obrigatório"}, status=400)
            if not telefone:
                return JsonResponse({"error": "O telefone é obrigatório"}, status=400)
            if not usuario_id:
                return JsonResponse({"error": "Usuário não encontrado"}, status=400)
            
            healthcenter = HealthCenter.objects.create(
                nome=nome,
                telefone=telefone
            )
            return JsonResponse({"success": "Centro de saúde cadastrado com sucesso"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Dados inválidos no corpo da requisição"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
def ReturnAllHealthCenters(request):
    if request.method == "GET":
        try:
            healthcenters = HealthCenter.objects.all()
            data = [{
                "id": healthcenter.id,
                "nome": healthcenter.nome,
                "telefone": healthcenter.telefone
            } for healthcenter in healthcenters]
            return JsonResponse({"Centros de Saúde": data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def GetHealthCenterById(request, healthcenter_id):
    if request.method == "GET":
        try:
            healthcenter = HealthCenter.objects.filter(id=healthcenter_id).first()
            if not healthcenter:
                return JsonResponse({'error': 'Centro de saúde não encontrado.'}, status=404)
            healthcenter_data = {
                'id': healthcenter.id,
                'nome': healthcenter.nome,
                'telefone': healthcenter.telefone,
                'created_at': healthcenter.created_at,
                'updated_at': healthcenter.updated_at
            }
            return JsonResponse({'Centro de Saúde': healthcenter_data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def DeleteHealthCenter(request, healthcenter_id):
    if request.method == "DELETE":
        try:
            healthcenter = HealthCenter.objects.filter(id=healthcenter_id).first()
            if not healthcenter:
                return JsonResponse({'error': 'Usuário não encontrado.'}, status=404)
            healthcenter.delete()
            return JsonResponse({'message': 'Usuário deletado com sucesso.'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def EditHealthCenter(request, healthcenter_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            nome = data.get("nome")
            telefone = data.get("telefone")
            healthcenter = HealthCenter.objects.filter(id=healthcenter_id).first()
            if not healthcenter:
                return JsonResponse({'error': 'Centro de saúde não encontrado.'}, status=404)
            if nome:
                healthcenter.nome = nome
            if telefone:
                healthcenter.telefone = telefone
            healthcenter.save()
            return JsonResponse({'message': 'Centro de saúde atualizado com sucesso.'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Dados inválidos no corpo da requisição.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
    