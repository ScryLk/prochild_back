from django.db import models
from categories.models import Categories
from django.utils.timezone import now


class Training(models.Model):
    id = models.AutoField(primary_key=True)
    categoria = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='trainings')
    titulo = models.CharField(max_length=150, null=False)
    descricao = models.TextField(blank=True, null=True)
    arquivo_nome = models.CharField(max_length=255, blank=True, null=True)
    arquivo_caminho = models.CharField(max_length=255, blank=True, null=True)
    tamanho = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo


class Download(models.Model):
    treinamento = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='downloads')
    dispositivo = models.CharField(max_length=50, blank=True, null=True)
    data_download = models.DateTimeField(default=now)

    def __str__(self):
        return f"Download do treinamento: {self.treinamento.titulo}"