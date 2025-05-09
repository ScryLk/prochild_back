from django.db import models
from sections.models import Section
from django.utils.timezone import now


class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    secao = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='categorias')
    nome = models.CharField(max_length=100, null=False)
    icone_id = models.CharField(max_length=50, blank=True, null=True)
    cor = models.CharField(max_length=7, blank=True, null=True)  # Novo campo para cor hexadecimal
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome