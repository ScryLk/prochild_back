from django.http import JsonResponse
from sections.models import Section
from .models import Categories
import json
from django.views.decorators.csrf import csrf_exempt
from users.decorators import admin_required  # Importa o decorador de admin


@csrf_exempt
def GetAllCategories(request):
    if request.method == "GET":
        try:
            categories_data = [
                {
                    'id': categorie.id,
                    'nome': categorie.nome,
                    'icone_id': categorie.icone_id,
                    'cor': categorie.cor,  # Adiciona o campo 'cor'
                    'secao_nome': categorie.secao.nome if categorie.secao else None,
                    'created_at': categorie.created_at,
                    'updated_at': categorie.updated_at
                }
                for categorie in Categories.objects.all()
            ]
            return JsonResponse({"success": categories_data})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def AddCategories(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            nome = data.get("nome")
            icone_id = data.get("icone_id")
            cor = data.get("cor")  # Adiciona o campo 'cor'
            secao_id = data.get("secao_id")
            if icone_id is None:
                return JsonResponse({"error": "O campo 'icone_id' é obrigatório"}, status=400)
            try:
                secao = Section.objects.get(id=secao_id)
            except Section.DoesNotExist:
                return JsonResponse({"error": "Seção não encontrada"}, status=404)
            categoria = Categories.objects.create(
                nome=nome,
                icone_id=icone_id,
                cor=cor,  # Salva o campo 'cor'
                secao=secao
            )
            return JsonResponse({"success": "Categoria criada com sucesso", "categoria_id": categoria.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Dados inválidos no corpo da requisição"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Método não permitido"}, status=405)


@csrf_exempt
def DeleteCategories(request, categories_id):
    if request.method == "DELETE":
        try:
            categorie = Categories.objects.filter(id=categories_id).first()
            if not categorie:
                return JsonResponse({"error": "Categoria não encontrada"}, status=404)
            categorie.delete()
            return JsonResponse({"success": "Categoria excluída com sucesso"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Método não permitido"}, status=405)


@csrf_exempt
def EditCategories(request, categories_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            categorie = Categories.objects.filter(id=categories_id).first()
            if not categorie:
                return JsonResponse({"error": "Categoria não encontrada"}, status=404)
            categorie.nome = data.get("nome") or categorie.nome
            categorie.icone_id = data.get("icone_id") or categorie.icone_id
            categorie.cor = data.get("cor") or categorie.cor  # Atualiza o campo 'cor'
            secao_id = data.get("secao_id")
            if secao_id:
                try:
                    secao = Section.objects.get(id=secao_id)
                    categorie.secao = secao
                except Section.DoesNotExist:
                    return JsonResponse({"error": "Seção não encontrada"}, status=404)
            categorie.save()
            return JsonResponse({"success": "Categoria atualizada com sucesso"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Dados inválidos no corpo da requisição"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Método não permitido"}, status=405)


@csrf_exempt
def GetCategorieBySection(request, section_id):
    if request.method == "GET":
        try:
            section = Section.objects.get(id=section_id)
            categories = Categories.objects.filter(secao=section)
            categorie_data = [
                {
                    'id': categorie.id,
                    'nome': categorie.nome,
                    'cor': categorie.cor,  # Adiciona o campo 'cor'
                    'created_at': categorie.created_at,
                    'updated_at': categorie.updated_at,
                    'secao_id': categorie.secao_id,
                    'icone_id': categorie.icone_id,
                }
                for categorie in categories
            ]
            return JsonResponse({"success": categorie_data}, status=200)
        except Section.DoesNotExist:
            return JsonResponse({"error": "Seção não encontrada"}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({"error": "Método não permitido"}, status=405)


@csrf_exempt
def GetCategorieById(request, categories_id):
    if request.method == "GET":
        try:
            categorie = Categories.objects.get(id=categories_id)
            categorie_data = {
                "id": categorie.id,
                "nome": categorie.nome,
                "icone_id": categorie.icone_id,
                "cor": categorie.cor,  # Adiciona o campo 'cor'
                "secao_id": categorie.secao.id,
                "created_at": categorie.created_at,
                "updated_at": categorie.updated_at,
            }
            return JsonResponse({"success": categorie_data}, status=200)
        except Categories.DoesNotExist:
            return JsonResponse({"error": "Categoria não encontrada"}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({"error": "Método não permitido"}, status=405)