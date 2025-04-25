from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import password_validation
from .models import User
import json
from django.views.decorators.csrf import csrf_exempt
from password_strength import PasswordPolicy
from django.contrib.auth.hashers import check_password


policy = PasswordPolicy.from_names(
    length=8,  # Mínimo de 8 caracteres
    uppercase=1,  # Pelo menos 1 letra maiúscula
    numbers=1,  # Pelo menos 1 número
    special=1,  # Pelo menos 1 caractere especial
    nonletters=0,  # Pelo menos 0 caracteres não alfabéticos
)

from django.contrib.auth.hashers import make_password

@csrf_exempt
def Cadastro(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            nome = data.get('nome')
            email = data.get('email')
            password_hash = data.get('password_hash')
            role = data.get('role', 'user')

            # Validações
            if not nome or not email or not password_hash:
                return JsonResponse({'error': 'Campos obrigatórios não preenchidos.'}, status=400)

            # Validação de senha
            errors = policy.test(password_hash)
            if errors:
                return JsonResponse({'error': 'Senha inválida. Certifique-se de que atende aos requisitos de segurança.'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email já está em uso.'}, status=400)

            hashed_password = make_password(password_hash)


            user = User.objects.create(
                nome=nome,
                email=email,
                password_hash=hashed_password,  
                role=role
            )

            return JsonResponse({'message': 'Usuário criado com sucesso!', 'id': user.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

@csrf_exempt
def Login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password_hash = data.get("password_hash")
            user = User.objects.filter(email=email).first()
            if not user:
                return JsonResponse({'error': 'Email ou senha inválidos.'}, status=401)

            if not check_password(password_hash, user.password_hash):
                return JsonResponse({'error': 'Email ou senha inválidos.'}, status=401)
            request.session['user_id'] = user.id
            request.session['user_nome'] = user.nome
            request.session['user_role'] = user.role

            return JsonResponse({'message': 'Usuário autenticado com sucesso!', 'id': user.id}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método não permitido.'}, status=405)
      
@csrf_exempt
def GetUserById(request, user_id):
    if request.method == "GET":
        try:
            # Buscar o usuário pelo ID
            user = User.objects.filter(id=user_id).first()
            if not user:
                return JsonResponse({'error': 'Usuário não encontrado.'}, status=404)

            # Retornar os dados do usuário
            user_data = {
                'id': user.id,
                'nome': user.nome,
                'email': user.email,
                'role': user.role,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            }
            return JsonResponse({'user': user_data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método não permitido.'}, status=405)
      
@csrf_exempt
def ReturnAllUsers(request):
    if request.method == "GET":
        try:
            users = User.objects.all()
            users_data = [
                {
                    'id': user.id,
                    'nome': user.nome,
                    'email': user.email,
                    'role': user.role,
                    'created_at': user.created_at,
                    'updated_at': user.updated_at
                }
                for user in users
            ]
            return JsonResponse({'users': users_data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método não permitido.'}, status=405)


@csrf_exempt
def DeleteUserById(request, user_id):
    if request.method == "DELETE":  # Alterado para usar o método HTTP DELETE
        try:
            # Buscar o usuário pelo ID
            user = User.objects.filter(id=user_id).first()
            if not user:
                return JsonResponse({'error': 'Usuário não encontrado.'}, status=404)

            # Deletar o usuário
            user.delete()

            return JsonResponse({'message': 'Usuário deletado com sucesso.'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método não permitido.'}, status=405)
  