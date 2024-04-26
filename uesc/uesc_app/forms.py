from django import forms
from django.contrib.auth.models import User
from .models import *


class LinkForm (forms.ModelForm):
    class Meta:
        model = Link
        fields = ['nome','endereco','grupo']
        labels = {'nome':'','endereco':'','grupo':''}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].widget = forms.TextInput()
        self.fields['nome'].widget.attrs.update(
            {'placeholder':"Titulo do Link", 'class': 'form-control'})
        self.fields['endereco'].widget.attrs.update(
            {'placeholder':"Endereço do Link", 'class': 'form-control'})
        self.fields['grupo'].widget.attrs.update(
            {'class': 'form-control'})

class GrupoForm (forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['tipo','titulo']
        labels = {'tipo':'','titulo':''}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['titulo'].widget.attrs.update(
            {'placeholder':"Titulo do Grupo", 'class': 'form-control'})
        self.fields['tipo'].widget.attrs.update(
            {'class': 'form-control'})


class TipoForm (forms.ModelForm):
    class Meta:
        model = Tipo
        fields = ['tipo']
        labels = {'tipo':''}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo'].widget.attrs.update(
            {'placeholder':"Titulo do Tipo", 'class': 'form-control'})



class LoginForm (forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]
        widgets = {'password': forms.PasswordInput()}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'placeholder':"Nome de Usuario", 'class': 'form-control'})
        self.fields['password'].widget.attrs.update(
            {'placeholder':"Senha", 'class': 'form-control'})
