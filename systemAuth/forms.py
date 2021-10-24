from django.contrib.auth.models import User
from django import forms
from .models import commonUserModel


class userForm(forms.ModelForm):
    class Meta:
        model = commonUserModel
        fields = ('userRut','userType',)
        labels = {
            'userRut': 'Rut',
            'userType': 'Tipo Usuario'
        }

class mainUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email','password',)
        labels = {
            'username': 'Usuario',
            'email': 'Correo',
            'password': 'contraseña', #poner widget de contrasena
        } 

