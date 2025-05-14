from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import User
from password_strength import PasswordPolicy
import json
import uuid
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from functools import wraps
from .decorators import login_required_json

# Política de senha
policy = PasswordPolicy.from_names(
    length=8,
    uppercase=1,
    numbers=1,
    special=1,
    nonletters=0,
)

@csrf_exempt
def Register(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

    try:
        data = json.loads(request.body)
        nome = data.get("nome")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "user")

        if not nome or not email or not password:
            return JsonResponse({'error': 'Campos obrigatórios não preenchidos.'}, status=400)

        if role not in ["admin", "user"]:
            return JsonResponse({'error': 'Role inválida.'}, status=400)

        if User.objects.filter(username=email).exists():
            return JsonResponse({'error': 'Email já está em uso.'}, status=400)

        errors = policy.test(password)
        if errors:
            return JsonResponse({'error': 'Senha inválida. Certifique-se de que atende aos requisitos de segurança.'}, status=400)

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=nome,
            role=role
        )
        return JsonResponse({'message': 'Usuário registrado com sucesso.', 'id': user.id}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def Login(request):
    if request.method == "GET":
        return JsonResponse({
            "error": "Não autenticado. Por favor, faça login."
        }, status=401)
        return JsonResponse({"detail": "Você deve estar autenticado para acessar esta página."}, status=401)    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({
                    "message": "Login realizado com sucesso.",
                    "id": user.id,
                    "name": user.first_name,
                    "email": user.email,
                    "role": user.role,
                })
            return JsonResponse({"error": "Credenciais inválidas."}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    if request.method != "POST":
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            print("Usuário autenticado?", request.user.is_authenticated)
            print("Usuário logado:", request.user.username)
            return JsonResponse({'message': 'Login realizado com sucesso.', 'id': user.id}, status=200)
        return JsonResponse({'error': 'Credenciais inválidas.'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def GetUserById(request, user_id):
    if request.method != "GET":
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

    try:
        user = User.objects.filter(id=user_id).first()
        if not user:
            return JsonResponse({'error': 'Usuário não encontrado.'}, status=404)

        user_data = {
            'id': user.id,
            'nome': user.first_name,
            'email': user.email,
            'role': user.role,
            'created_at': user.date_joined,
            'updated_at': user.last_login
        }
        return JsonResponse({'user': user_data}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def Logout(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

    logout(request)
    return JsonResponse({'message': 'Logout realizado com sucesso.'}, status=200)


def ReturnAllUsers(request):
    print("DEBUG AUTH:", request.user.is_authenticated, request.user)
    print("Usuário autenticado?", request.user.is_authenticated)
    print("Usuário logado:", request.user.username)
    users = User.objects.all()
    data = [{
        "id": u.id,
        "nome": u.first_name,
        "email": u.email,
        "role": u.role,
        "created_at": u.date_joined,
        "updated_at": u.last_login,
    } for u in users]
    return JsonResponse({'users': data}, status=200)


@csrf_exempt
def DeleteUserById(request, user_id):
    if request.method != "DELETE":
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

    try:
        user = User.objects.filter(id=user_id).first()
        if not user:
            return JsonResponse({'error': 'Usuário não encontrado.'}, status=404)

        user.delete()
        return JsonResponse({'message': 'Usuário deletado com sucesso.'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def ResetPassword(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get("email")

        user = User.objects.filter(email=email).first()
        if not user:
            return JsonResponse({'error': 'E-mail inexistente.'}, status=404)

        reset_token = str(uuid.uuid4())
        reset_token_expires = timezone.now() + timedelta(hours=1)
        user.reset_token = reset_token
        user.reset_token_expires = reset_token_expires
        user.save()

        return JsonResponse({
            'message': 'Token de redefinição de senha gerado com sucesso.',
            'reset_token': reset_token
        }, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def SetNewPassword(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

    try:
        data = json.loads(request.body)
        reset_token = data.get("reset_token")
        new_password = data.get("new_password")

        if not reset_token or not new_password:
            return JsonResponse({'error': 'Token e nova senha são obrigatórios.'}, status=400)

        user = User.objects.filter(reset_token=reset_token).first()
        if not user:
            return JsonResponse({'error': 'Token inválido.'}, status=404)

        if user.reset_token_expires < timezone.now():
            return JsonResponse({'error': 'Token expirado.'}, status=400)

        errors = policy.test(new_password)
        if errors:
            return JsonResponse({'error': 'Senha inválida. Certifique-se de que atende aos requisitos de segurança.'}, status=400)

        user.set_password(new_password)
        user.reset_token = None
        user.reset_token_expires = None
        user.save()

        return JsonResponse({'message': 'Senha redefinida com sucesso.'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def EditUser(request, user_id):
    if request.method != "PUT":
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

    try:
        # Verificar se o usuário existe
        user = User.objects.filter(id=user_id).first()
        if not user:
            return JsonResponse({'error': 'Usuário não encontrado.'}, status=404)

        # Carregar os dados enviados no corpo da requisição
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Erro ao decodificar JSON. Verifique o formato da requisição.'}, status=400)

        # Atualizar os campos permitidos
        nome = data.get("nome")
        email = data.get("email")
        role = data.get("role")

        # Validar e atualizar o nome
        if nome:
            user.first_name = nome

        # Validar e atualizar o email
        if email:
            if User.objects.filter(email=email).exclude(id=user_id).exists():
                return JsonResponse({'error': 'Email já está em uso.'}, status=400)
            user.email = email

        # Validar e atualizar o role
        if role:
            if role not in dict(User._meta.get_field('role').choices).keys():
                return JsonResponse({'error': 'Role inválida. Use "admin" ou "user".'}, status=400)
            user.role = role

        # Salvar as alterações
        user.save()

        # Retornar os dados atualizados do usuário
        user_data = {
            'id': user.id,
            'nome': user.first_name,
            'email': user.email,
            'role': user.role,
            'created_at': user.date_joined,
            'updated_at': user.last_login
        }
        return JsonResponse({"success": user_data}, status=200)

    except Exception as e:
        return JsonResponse({'error': f'Erro interno: {str(e)}'}, status=500)
    if request.method != "PUT":
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

    try:
        # Verificar se o usuário existe
        user = User.objects.filter(id=user_id).first()
        if not user:
            return JsonResponse({'error': 'Usuário não encontrado.'}, status=404)

        # Carregar os dados enviados no corpo da requisição
        data = json.loads(request.body)

        # Atualizar os campos permitidos
        nome = data.get("nome")
        email = data.get("email")
        role = data.get("role")

        # Validar o nome
        if nome:
            user.first_name = nome

        # Validar o email
        if email:
            if User.objects.filter(email=email).exclude(id=user_id).exists():
                return JsonResponse({'error': 'Email já está em uso.'}, status=400)
            user.email = email

        # Validar o role
        if role:
            if role not in ["admin", "user"]:
                return JsonResponse({'error': 'Role inválida. Use "admin" ou "user".'}, status=400)
            user.role = role

        # Salvar as alterações
        user.save()

        # Retornar os dados atualizados do usuário
        user_data = {
            'id': user.id,
            'nome': user.first_name,
            'email': user.email,
            'role': user.role,
            'created_at': user.date_joined,
            'updated_at': user.last_login
        }
        return JsonResponse({"success": user_data}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Erro ao decodificar JSON. Verifique o formato da requisição.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Erro interno: {str(e)}'}, status=500)
    if request.method != "PUT":
        return JsonResponse({'error': 'Método não permitido.'}, status=405)
    try:
        data = json.loads(request.body)
        user = User.objects.filter(id=user_id).first()
        if not user:
            return JsonResponse({'error': 'Usuário não encontrado.'}, status=404)
        nome = data.get("nome")
        email = data.get("email")
        role = data.get("role")
        if nome:
            user.first_name = nome
        if email:
            user.email = email
        if role in ["admin", "user"]:
            user.role = role
        user.save()
        user_data = {
            'id': user.id,
            'nome': user.first_name,
            'email': user.email,
            'role': user.role,
            'created_at': user.date_joined,
            'updated_at': user.last_login
        }
        return JsonResponse({"success": user_data}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)