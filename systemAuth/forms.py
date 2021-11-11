from django.contrib.auth.models import User
from django import forms
from django.db.models import fields
from django.forms import widgets
from django.forms.fields import CharField
from .models import commonUserModel
from django.contrib.auth.forms import AuthenticationForm


class paymentForm(forms.Form):
    fields = ('order','paymentType',)
    labels = {
            'order': 'orden',
            'paymentType': 'Tipo Pago',
    }
    widgets = {
        'paymentType': forms.Select(attrs={'class': 'btn btn-secondary dropdown-toggle'}),
    }


class orderForm(forms.Form):
    userID = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}), label="ID de usuario")
    orderType = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}), label="Tipo de orden")
    #nextPayment = forms.DateInput(widget = widgets.DateTimeInput(format)) # widget= forms.DateTimeInput() , label="Fecha proximo pago"
    amount = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control form control-alternative'}), label="plata")
    employeeID = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}), label="ID de empleado")
  #  dateVisit = forms.DateTimeInput ()#widget=forms.DateTimeInput(), label="fecha visita"
    orderDescription = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}), label="orden description")


    labels = {
            'userID':  'ID usuario',
            'orderType': 'Tipo de Orden',
            'nextPayment': 'Siguiente fecha de pago',
            'amount': 'Monto a pagar',
            'employeeID': 'Profesional Asignado',
            'dateVisit': 'Fecha visita',
            'orderDescription': 'Descripcion',
    }
    widgets = {
            'orderType': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
            'nextPayment': forms.DateTimeInput(attrs={'class': 'form-control form control-alternative'}),
            #'amount': forms.NumberInput(attrs={'class': 'form-control form control-alternative'}),
            'employeeID': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
            'dateVisit': forms.DateTimeInput(attrs={'class': 'form-control form control-alternative'}),
            'orderDescription': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
    }



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