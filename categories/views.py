from django.db import models
from django.http import JsonResponse
import json

def GetAllCategories(request):
  if request.method == "GET":
    try:
      return JsonResponse({"success": "success"})
    except:
      return JsonResponse({"error": "error"})


def AddCategories(request):
  if request.method == "GET":
    try:
      return JsonResponse({"success": "success"})
    except:
      return JsonResponse({"error": "error"})
