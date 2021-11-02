from django.contrib.auth.models import User
from django import forms
from django.forms import widgets
from .models import commonUserModel
from django.contrib.auth.forms import AuthenticationForm


class userForm(forms.ModelForm):
    class Meta:
        model = commonUserModel
        fields = ('userFirstName','userLastName','userAge','userPhoneNumber','userAddress','userRut','userType',)
        labels = {
            'userFirstName': 'Nombre',
            'userLastName': 'Apellido',
            'userAge': 'Edad',
            'userPhoneNumber': 'Numero de Celular',
            'userAddress': 'Direccion',
            'userRut': 'Rut',
            'userType': 'Tipo Usuario',
        }
        widgets = {
            'userFirstName': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
            'userLastName': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
            'userAge': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
            'userPhoneNumber': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
            'userAddress': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
            'userRut': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
            'userType': forms.Select(attrs={'class': 'btn btn-primary dropdown-toggle'}),
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
        help_texts = {
            'username': None,
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
            'email': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control form control-alternative'}),
        }

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Usuario', 'id': 'hello'}))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Contrasena', }))