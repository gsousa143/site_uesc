from django.db import models

class Tipo(models.Model):
    tipo = models.CharField(max_length=100)

    def __str__(self):
        return self.tipo


class Grupo(models.Model):
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    data = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo
    

class Link(models.Model):
    nome = models.TextField(null=True)
    endereco = models.CharField(max_length=200)
    grupo = models.ForeignKey(Grupo,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome
    
