from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Training, Favorite
from categories.models import Categories
from sections.models import Section
from django.views.decorators.csrf import csrf_exempt
from users.decorators import admin_required  
from django.contrib.auth import get_user_model


@csrf_exempt
def AddTrainings(request):
    if request.method == "POST":
        try:
            titulo = request.POST.get("titulo")
            descricao = request.POST.get("descricao")
            categoria_id = request.POST.get("categoria_id")
            arquivo = request.FILES.get("arquivo_caminho")  # Obtém o arquivo enviado

            # Validações
            if not titulo:
                return JsonResponse({"error": "Titulo Obrigatório"}, status=400)
            if not descricao:
                return JsonResponse({"error": "Descrição Obrigatória"}, status=400)
            if not categoria_id:
                return JsonResponse({"error": "Categoria Obrigatória"}, status=400)
            if not arquivo:
                return JsonResponse({"error": "Arquivo Obrigatório"}, status=400)

            # Verifica o tipo de arquivo
            if arquivo.content_type not in ["application/pdf", "image/png", "video/mp4"]:
                return JsonResponse({"error": "Tipo de arquivo não suportado. Apenas PDF, PNG e MP4 são permitidos."}, status=400)

            # Obtém a categoria e a seção associada
            try:
                categoria = Categories.objects.get(id=categoria_id)
                secao = categoria.secao  # Obtém a seção associada à categoria
                if not secao:
                    return JsonResponse({"error": "A seção associada à categoria não existe"}, status=404)
            except Categories.DoesNotExist:
                return JsonResponse({"error": "Categoria não encontrada"}, status=404)

            # Cria o treinamento
            training = Training.objects.create(
                titulo=titulo,
                descricao=descricao,
                categoria=categoria,
                secao=secao,
                arquivo_nome=arquivo.name,
                arquivo_caminho=arquivo  # Salva o arquivo no campo FileField
            )
            return JsonResponse({"success": "Treinamento cadastrado com sucesso", "training_id": training.id}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Método não permitido"}, status=405)
    
    if request.method == "POST":
        try:
            titulo = request.POST.get("titulo")
            descricao = request.POST.get("descricao")
            categoria_id = request.POST.get("categoria_id")
            arquivo = request.FILES.get("arquivo")  
            if not titulo:
                return JsonResponse({"error": "Titulo Obrigatório"}, status=400)
            if not descricao:
                return JsonResponse({"error": "Descrição Obrigatória"}, status=400)
            if not categoria_id:
                return JsonResponse({"error": "Categoria Obrigatória"}, status=400)
            if not arquivo:
                return JsonResponse({"error": "Arquivo Obrigatório"}, status=400)
            if arquivo.content_type not in ["application/pdf", "image/png", "video/mp4"]:
                return JsonResponse({"error": "Tipo de arquivo não suportado. Apenas PDF, PNG e MP4 são permitidos."}, status=400)
            try:
                categoria = Categories.objects.get(id=categoria_id)
                secao = categoria.secao  
                if not secao:
                    return JsonResponse({"error": "A seção associada à categoria não existe"}, status=404)
            except Categories.DoesNotExist:
                return JsonResponse({"error": "Categoria não encontrada"}, status=404)

            training = Training.objects.create(
                titulo=titulo,
                descricao=descricao,
                categoria=categoria,
                secao=secao,
                arquivo_nome=arquivo.name,
                arquivo_caminho=arquivo  
            )
            return JsonResponse({"success": "Treinamento cadastrado com sucesso", "training_id": training.id}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Método não permitido"}, status=405)
    if request.method == "POST":
        try:
            data = json.loads(request.body)  
            titulo = data.get("titulo")
            descricao = data.get("descricao")
            arquivo_nome = data.get("arquivo_nome")
            arquivo_caminho = data.get("arquivo_caminho")
            tamanho = data.get("tamanho")
            categoria_id = data.get("categoria_id")

            # Validações
            if not titulo:
                return JsonResponse({"error": "Titulo Obrigatório"}, status=400)
            if not descricao:
                return JsonResponse({"error": "Descrição Obrigatória"}, status=400)
            if not categoria_id:
                return JsonResponse({"error": "Categoria Obrigatória"}, status=400)

            try:
                categoria = Categories.objects.get(id=categoria_id)
                secao = categoria.secao 
                if not secao:
                    return JsonResponse({"error": "A seção associada à categoria não existe"}, status=404)
            except Categories.DoesNotExist:
                return JsonResponse({"error": "Categoria não encontrada"}, status=404)
            training = Training.objects.create(
                titulo=titulo,
                descricao=descricao,
                arquivo_nome=arquivo_nome,
                arquivo_caminho=arquivo_caminho,
                tamanho=tamanho,
                categoria=categoria,
                secao=secao 
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
                    'arquivo_caminho': request.build_absolute_uri(training.arquivo_caminho.url) if training.arquivo_caminho else None,  # Retorna a URL absoluta                    'categoria_id': training.categoria.id if training.categoria else None,
                    'categoria_nome': training.categoria.nome if training.categoria else None,
                    'secao_id': training.secao.id if training.secao else None,
                    'secao_nome': training.secao.nome if training.secao else None,
                    'created_at': training.created_at,
                    'updated_at': training.updated_at
                }
                for training in trainings 
            ]
            return JsonResponse({"success": training_data}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
@csrf_exempt
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
def EditTraining(request, training_id):
    if request.method == "PUT":
        try:
            # Obtém o treinamento pelo ID
            try:
                training = Training.objects.get(id=training_id)
            except Training.DoesNotExist:
                return JsonResponse({"error": "Treinamento não encontrado"}, status=404)

            # Processa os dados enviados no corpo da requisição
            data = json.loads(request.body.decode("utf-8"))  # Decodifica o JSON enviado
            titulo = data.get("titulo")
            descricao = data.get("descricao")
            categoria_id = data.get("categoria_id")
            tamanho = data.get("tamanho")

            # Atualiza os campos do treinamento
            if titulo:
                training.titulo = titulo
            if descricao:
                training.descricao = descricao
            if tamanho:
                training.tamanho = tamanho

            # Atualiza a categoria e a seção associada
            if categoria_id:
                try:
                    categoria = Categories.objects.get(id=categoria_id)
                    secao = categoria.secao
                    if not secao:
                        return JsonResponse({"error": "A seção associada à categoria não existe"}, status=404)
                    training.categoria = categoria
                    training.secao = secao  
                except Categories.DoesNotExist:
                    return JsonResponse({"error": "Categoria não encontrada"}, status=404)
            arquivo = request.FILES.get("arquivo_caminho") 
            if arquivo:
                if arquivo.content_type not in ["application/pdf", "image/png", "video/mp4"]:
                    return JsonResponse({"error": "Tipo de arquivo não suportado. Apenas PDF, PNG e MP4 são permitidos."}, status=400)
                training.arquivo_nome = arquivo.name
                training.arquivo_caminho = arquivo  
            training.save()

            training_data = {
                "id": training.id,
                "titulo": training.titulo,
                "descricao": training.descricao,
                "arquivo_nome": training.arquivo_nome,
                "arquivo_caminho": request.build_absolute_uri(training.arquivo_caminho.url) if training.arquivo_caminho else None,
                "tamanho": training.tamanho,
                "categoria_id": training.categoria.id if training.categoria else None,
                "secao_id": training.secao.id if training.secao else None,
                "created_at": training.created_at,
                "updated_at": training.updated_at,
            }
            return JsonResponse({"success": "Treinamento atualizado com sucesso", "training": training_data}, status=200)

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
                "arquivo_caminho": request.build_absolute_uri(training.arquivo_caminho.url) if training.arquivo_caminho else None,  # Converte para URL
                "tamanho": training.tamanho,
                "categoria_id": training.categoria.id if training.categoria else None,
                "secao_id": training.secao.id if training.secao else None,
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
            # Obtém a categoria pelo ID
            categorie = Categories.objects.get(id=categorie_id)
            
            # Filtra os treinamentos pela categoria
            trainings = Training.objects.filter(categoria=categorie)
            
            # Prepara os dados dos treinamentos
            trainings_data = [
                {
                    'id': training.id, 
                    'titulo': training.titulo, 
                    'descricao': training.descricao,
                    'arquivo_nome': training.arquivo_nome, 
                    'arquivo_caminho': request.build_absolute_uri(training.arquivo_caminho.url) if training.arquivo_caminho else None,  
                    'tamanho': training.tamanho,
                    'categoria_id': training.categoria.id if training.categoria else None,
                    'categoria_nome': training.categoria.nome if training.categoria else None, 
                    'secao_id': training.secao.id if training.secao else None,
                    'secao_nome': training.secao.nome if training.secao else None,  
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

@csrf_exempt
def GetFavoritesByUser(request, user_id):
    if request.method == "GET":
        try:
            favorites = Favorite.objects.filter(user_id=user_id).select_related('training')
            favorites_data = [
                {
                    'id': fav.training.id,
                    'titulo': fav.training.titulo,
                    'descricao': fav.training.descricao,
                    'arquivo_nome': fav.training.arquivo_nome,
                    'arquivo_caminho': request.build_absolute_uri(fav.training.arquivo_caminho.url) if fav.training.arquivo_caminho else None,
                    'tamanho': fav.training.tamanho,
                    'categoria_id': fav.training.categoria.id if fav.training.categoria else None,
                    'categoria_nome': fav.training.categoria.nome if fav.training.categoria else None,
                    'secao_id': fav.training.secao.id if fav.training.secao else None,
                    'secao_nome': fav.training.secao.nome if fav.training.secao else None,
                    'created_at': fav.training.created_at,
                    'updated_at': fav.training.updated_at
                }
                for fav in favorites
            ]
            return JsonResponse({"success": favorites_data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método não permitido.'}, status=405)
    
@csrf_exempt
def FavoriteTrainings(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            training_id = data.get("training_id")
            if not user_id or not training_id:
                return JsonResponse({'error': 'user_id e training_id são obrigatórios.'}, status=400)
            
            User = get_user_model()
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'error': 'Usuário não encontrado.'}, status=404)
            try:
                training = Training.objects.get(id=training_id)
            except Training.DoesNotExist:
                return JsonResponse({'error': 'Treinamento não encontrado.'}, status=404)
            
            fav, created = Favorite.objects.get_or_create(user=user, training=training)
            if created:
                return JsonResponse({'success': 'Treinamento favoritado!'}, status=201)
            else:
                return JsonResponse({'info': 'Já está favoritado.'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

@csrf_exempt
def UnfavoriteTrainings(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            training_id = data.get("training_id")
            if not user_id or not training_id:
                return JsonResponse({'error': 'user_id e training_id são obrigatórios.'}, status=400)

            User = get_user_model()
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'error': 'Usuário não encontrado.'}, status=404)
            try:
                fav = Favorite.objects.get(user=user, training_id=training_id)
            except Favorite.DoesNotExist:
                return JsonResponse({'error': 'Favorito não encontrado.'}, status=404)

            fav.delete()
            return JsonResponse({'success': 'Treinamento removido dos favoritos.'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método não permitido.'}, status=405)



