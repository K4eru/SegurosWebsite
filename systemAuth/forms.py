from django.contrib.auth.models import User
from django import forms
from systemAuth import views
from .models import commonUserModel 
from django.contrib.auth.forms import AuthenticationForm
import requests, re ,json
from systemCore.services import get_companies

#TUPLES
RESPONSABLES_CHOICES = []

try:
    responsables = commonUserModel.get_responsables()
    for res in responsables:
        RESPONSABLES_CHOICES.append(tuple((getattr(res, 'id'), getattr(res, 'firstName') +' '+ getattr(res, 'lastName'))))
except:
    print("No existen profesionales")

CLIENT_CHOICES = []

try:
    responsables = commonUserModel.get_clients()
    for res in responsables:
        CLIENT_CHOICES.append(tuple((getattr(res, 'id'), getattr(res, 'firstName') +' '+ getattr(res, 'lastName'))))
        
    # print(CLIENT_CHOICES)   
except:
    print("No existen clientes")

ORDER_TYPES = ((0, 'Normal' ),
                (1, 'Especial'))


class userForm(forms.ModelForm):

    def __init__(self ,*args, **kwargs):
        super().__init__(*args, **kwargs)
        companies = get_companies()

        COMPANY = []
        for comp in companies:
            COMPANY.append(tuple((comp["id"], comp["name"])))

        self.fields['company'].choices = COMPANY
    
    company = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'btn btn-secondary dropdown-toggle'}), label="Compañia")
    class Meta:
        model = commonUserModel
        fields = ('firstName','lastName','phoneNumber','rut','userType',)
        labels = {
            'firstName': 'Nombre',
            'lastName': 'Apellido',
            'phoneNumber': 'Numero de Celular',
            'rut': 'Rut',
            'userType': 'Tipo Usuario',
        }
        widgets = {
            'firstName': forms.TextInput(attrs={'class': 'form-control form control-alternative', 'id':'fn'}),
            'lastName': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
            'rut': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
            'userType': forms.Select(attrs={'class': 'btn btn-secondary dropdown-toggle'}),
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


