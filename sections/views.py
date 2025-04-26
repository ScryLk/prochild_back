from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Section
import json
from django.contrib.auth.decorators import login_required


@csrf_exempt
def AddSections(request):
  if request.method == "POST":
    try:
      data = json.loads(request.body)
      nome = data.get("nome")
      if not nome:
        return JsonResponse({"Error": "O nome da Seção é obrigatório"}, status=400)
      else:
        Section.nome = nome
        Section.objects.create(nome = nome)
        return JsonResponse({"Success": "Seção cadastrada com sucesso"}, status=201)
    except:
      return JsonResponse({"Error": "Metodo não permitido"}, status=405)


@csrf_exempt
def ReturnAllSections(request):
  if request.method == "GET":
    try:
      sections = Section.objects.all()
      users_data = [
                {
                    'id': section.id,
                    'nome': section.nome,
                    'created_at': section.created_at,
                    'updated_at': section.updated_at
                }
                for section in sections
            ]
      return JsonResponse({"Sucesso": users_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def DeleteSections(request, sections_id):
  if request.method == "DELETE":
    try:
        section = Section.objects.filter(id=sections_id).first()
        if not section:
          return JsonResponse({"Error": "Section não encontrada"})
        section.delete()
        return JsonResponse({"Success": "Section Excluida com sucesso"})
    except:
      return JsonResponse({"Error": "Método não permitido"})


@csrf_exempt
def EditSections(request, sections_id):
  if request.method == "PUT":
    try:
      data = json.loads(request.body)
      section = Section.objects.filter(id=sections_id).first()
      section.nome = data.get("nome") or section.name
      section.save()
      section_data = [{
        'id': section.id,
        'nome': section.nome,
        'created_at': section.created_at,
        'updated_at': section.updated_at
      }]
      return JsonResponse({"Success": section_data})
    except:
      return JsonResponse({"Error": "Método não permitido"})
