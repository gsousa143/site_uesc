from django import forms
from .models import *


class LinkForm (forms.ModelForm):
    class Meta:
        model = Link
        fields = ['nome','endereco','grupo']
    
class GrupoForm (forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['tipo','titulo']


class TipoForm (forms.ModelForm):
    class Meta:
        model = Tipo
        fields = ['tipo']
