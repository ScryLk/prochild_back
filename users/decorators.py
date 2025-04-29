from functools import wraps
from django.http import JsonResponse
from .models import User


def custom_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return JsonResponse({'error': 'Usuário não autenticado.'}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'error': 'Usuário não autenticado.'}, status=404)
        user = User.objects.filter(id=user_id).first()
        if not user or user.role != 'admin':
            return JsonResponse({'error': 'Acesso negado. Permissão de administrador necessária.'}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view
 