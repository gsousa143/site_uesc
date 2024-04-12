from django.db import models

class Resultado(models.Model):
    nome = models.CharField(max_length=200)
    titulo = models.CharField(max_length=200)
    data = models.DateField(auto_now_add=True)
    link = models.CharField(max_length=200)
    obs = models.CharField(max_length=200)

    def __str__(self):
        return self.nome