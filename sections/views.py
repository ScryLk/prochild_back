from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Section
import json
from users.decorators import admin_required 

@csrf_exempt
@admin_required
def AddSections(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            nome = data.get("nome")
            if not nome:
                return JsonResponse({"Error": "O nome da Seção é obrigatório"}, status=400)
            else:
                Section.objects.create(nome=nome)
                return JsonResponse({"Success": "Seção cadastrada com sucesso"}, status=201)
        except Exception as e:
            return JsonResponse({"Error": str(e)}, status=500)
    else:
        return JsonResponse({"Error": "Método não permitido"}, status=405)

@csrf_exempt
def ReturnAllSections(request):
    if request.method == "GET":
        try:
            sections = Section.objects.all()
            sections_data = [
                {
                    'id': section.id,
                    'nome': section.nome,
                    'created_at': section.created_at,
                    'updated_at': section.updated_at
                }
                for section in sections
            ]
            return JsonResponse({"Sucesso": sections_data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({"Error": "Método não permitido"}, status=405)

@csrf_exempt
@admin_required
def DeleteSections(request, sections_id):
    if request.method == "DELETE":
        try:
            section = Section.objects.filter(id=sections_id).first()
            if not section:
                return JsonResponse({"Error": "Seção não encontrada"}, status=404)
            section.delete()
            return JsonResponse({"Success": "Seção excluída com sucesso"}, status=200)
        except Exception as e:
            return JsonResponse({"Error": str(e)}, status=500)
    else:
        return JsonResponse({"Error": "Método não permitido"}, status=405)

@csrf_exempt
@admin_required
def EditSections(request, sections_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            section = Section.objects.filter(id=sections_id).first()
            if not section:
                return JsonResponse({"Error": "Seção não encontrada"}, status=404)
            section.nome = data.get("nome") or section.nome
            section.save()
            section_data = {
                'id': section.id,
                'nome': section.nome,
                'created_at': section.created_at,
                'updated_at': section.updated_at
            }
            return JsonResponse({"Success": section_data}, status=200)
        except Exception as e:
            return JsonResponse({"Error": str(e)}, status=500)
    else:
        return JsonResponse({"Error": "Método não permitido"}, status=405)

@admin_required
def GetSectionsById(request, sections_id):
  if request.method == "GET":
    try:
      section = Section.objects.filter(id=sections_id)
      if not section:
        return JsonResponse({"error": "Section não encontrada"}, status=404)
      section_data = [
        {
          "id": section.id, 
          "nome": section.nome, 
          "created_at": section.created_at, 
          "updated_at": section.updated_at
        }
      ]
      return JsonResponse({"success": section_data})
    except Exception as e:
            return JsonResponse({"Error": str(e)}, status=500)
    else:
        return JsonResponse({"Error": "Método não permitido"}, status=405)