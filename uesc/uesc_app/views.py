from django.shortcuts import render
from uesc_app.models import Resultado

def home(request):
    resultado = Resultado.objects.order_by('id')
    contexto = {'resultado':resultado}
    return render(request,"index.html", contexto)
