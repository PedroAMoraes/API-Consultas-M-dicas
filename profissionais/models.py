from django.db import models

# Create your models here.
class Profissional(models.Model):
    nome_social = models.CharField(max_length=255, null=False)
    profissao = models.CharField(max_length=255, null=False)
    endereco = models.CharField(max_length=255, null=False)
    contato = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.nome_social