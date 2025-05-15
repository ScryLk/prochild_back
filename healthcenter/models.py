from django.db import models

# Importando diretamente o modelo users.User
from users.models import User

class HealthCenter(models.Model):
    nome = models.CharField(max_length=150)
    telefone = models.CharField(max_length=20, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='centros_de_saude')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome