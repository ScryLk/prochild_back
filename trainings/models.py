from django.db import models
from categories.models import Categories
from django.utils.timezone import now
from sections.models import Section
from django.conf import settings


class Training(models.Model):
    id = models.AutoField(primary_key=True)
    categoria = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='trainings')
    titulo = models.CharField(max_length=150, null=False)
    descricao = models.TextField(blank=True, null=True)
    secao = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="trainings",
        null=True,  
        blank=True  
    )
    arquivo_nome = models.CharField(max_length=255, blank=True, null=True)
    arquivo_caminho = models.FileField(upload_to='trainings/files/', blank=True, null=True)  # Diretório para armazenar arquivos
    tamanho = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'training')

    def __str__(self):
        return f"{self.user} favoritou {self.training}"