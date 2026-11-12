from django.db import models

# Create your models here.
class Profissional(models.Model):
    nome = models.CharField(max_length=255)
    profissao = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    contato = models.CharField(max_length=255)

    def __str__(self):
        return self.name