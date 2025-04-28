from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Training
from categories.models import Categories
from django.views.decorators.csrf import csrf_exempt
from users.decorators import admin_required  # Importa o decorador de admin

@csrf_exempt
@admin_required
def AddTrainings(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  
            titulo = data.get("titulo")
            descricao = data.get("descricao")
            arquivo_nome = data.get("arquivo_nome")
            arquivo_caminho = data.get("arquivo_caminho")
            tamanho = data.get("tamanho")
            categoria_id = data.get("categoria_id")
            if not titulo:
                return JsonResponse({"error": "Titulo Obrigatório"}, status=400)
            if not descricao:
                return JsonResponse({"error": "Descrição Obrigatória"}, status=400)
            if not categoria_id:
                return JsonResponse({"error": "Categoria Obrigatória"}, status=400)
            try:
                categoria = Categories.objects.get(id=categoria_id)
            except Categories.DoesNotExist:
                return JsonResponse({"error": "Categoria não encontrada"}, status=404)
            training = Training.objects.create(
                titulo=titulo,
                descricao=descricao,
                arquivo_nome=arquivo_nome,
                arquivo_caminho=arquivo_caminho,
                tamanho=tamanho,
                categoria=categoria
            )
            return JsonResponse({"success": "Treinamento cadastrado com sucesso", "training_id": training.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Dados inválidos no corpo da requisição"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Método não permitido"}, status=405)

def ReturnAllTrainings(request):
    if request.method == "GET":
        try:
            trainings = Training.objects.all()
            training_data = [
                {
                    'id': training.id,
                    'titulo': training.titulo, 
                    'tamanho': training.tamanho,
                    'descricao': training.descricao,
                    'arquivo_nome': training.arquivo_nome,
                    'arquivo_caminho': training.arquivo_caminho,
                    'created_at': training.created_at,
                    'updated_at': training.updated_at,
                    'categoria_id': training.categoria_id      
                }
                for training in trainings 
            ]
            return JsonResponse({"Success": training_data})
        except Exception as e:
            return JsonResponse({"Error": str(e)}, status=500)

@csrf_exempt
@admin_required
def DeleteTraining(request, training_id):
    if request.method == "DELETE":
        try:
            training = Training.objects.filter(id=training_id).first()
            if not training:
                return JsonResponse({"error": "Treinamento não encontrado"}, status=404)
            training.delete()
            return JsonResponse({"success": "Treinamento deletado com sucesso"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Método não permitido"}, status=405)

@csrf_exempt
@admin_required
def EditTraining(request, training_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)  
            try:
                training = Training.objects.get(id=training_id) 
            except Training.DoesNotExist:
                return JsonResponse({"error": "Treinamento não encontrado"}, status=404)
            training.titulo = data.get("titulo", training.titulo)
            training.descricao = data.get("descricao", training.descricao)
            training.arquivo_nome = data.get("arquivo_nome", training.arquivo_nome)
            training.arquivo_caminho = data.get("arquivo_caminho", training.arquivo_caminho)
            training.tamanho = data.get("tamanho", training.tamanho)
            categoria_id = data.get("categoria_id")
            if categoria_id:
                try:
                    categoria = Categories.objects.get(id=categoria_id)
                    training.categoria = categoria
                except Categories.DoesNotExist:
                    return JsonResponse({"error": "Categoria não encontrada"}, status=404)
            training.save()
            training_data = {
                "id": training.id,
                "titulo": training.titulo,
                "descricao": training.descricao,
                "arquivo_nome": training.arquivo_nome,
                "arquivo_caminho": training.arquivo_caminho,
                "tamanho": training.tamanho,
                "categoria_id": training.categoria.id,
                "created_at": training.created_at,
                "updated_at": training.updated_at,
            }
            return JsonResponse({"success": "Treinamento atualizado com sucesso", "training": training_data}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Dados inválidos no corpo da requisição"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Método não permitido"}, status=405)

def GetTrainingById(request, training_id):
    if request.method == "GET":
        try:
            training = Training.objects.get(id=training_id)
            training_data = {
                "id": training.id,
                "titulo": training.titulo,
                "descricao": training.descricao,
                "arquivo_nome": training.arquivo_nome,
                "arquivo_caminho": training.arquivo_caminho,
                "tamanho": training.tamanho,
                "categoria_id": training.categoria.id,
                "created_at": training.created_at,
                "updated_at": training.updated_at,
            }
            return JsonResponse({"success": training_data}, status=200)
        except Training.DoesNotExist:
            return JsonResponse({"error": "Treinamento não encontrado"}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({"error": "Método não permitido"}, status=405)

@csrf_exempt
@admin_required
def DeleteAllTrainings(request, categorie_id):
    if request.method == "DELETE":
        try:
            categorie = Categories.objects.get(id=categorie_id)
            trainings = Training.objects.filter(categoria=categorie)
            trainings.delete()
            return JsonResponse({"success": "Todos os treinamentos da categoria foram deletados com sucesso"}, status=200)
        except Categories.DoesNotExist:
            return JsonResponse({"error": "Categoria não encontrada"}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({"error": "Método não permitido"}, status=405)

def GetTrainingByCategories(request, categorie_id):
    if request.method == "GET":
        try:
            categorie = Categories.objects.get(id=categorie_id)
            trainings = Training.objects.filter(categoria=categorie)
            trainings_data = [
                {
                    'id': training.id, 
                    'titulo': training.titulo, 
                    'descricao': training.descricao,
                    'arquivo_nome': training.arquivo_nome, 
                    'arquivo_caminho': training.arquivo_caminho, 
                    'tamanho': training.tamanho,
                    'categoria_id': training.categoria_id,
                    'created_at': training.created_at,
                    'updated_at': training.updated_at
                }
                for training in trainings
            ]
            return JsonResponse({"success": trainings_data}, status=200)
        except Categories.DoesNotExist:
            return JsonResponse({"error": "Categoria não encontrada"}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({"error": "Método não permitido"}, status=405)