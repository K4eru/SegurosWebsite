from django.contrib.auth.models import User
from django import forms
from .models import commonUserModel, company
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

class DateInput(forms.DateInput):
    input_type = 'date'

class orderForm(forms.Form):
    userID = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}), label="ID de usuario")
    orderType = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}), label="Tipo de orden")
    nextPayment = forms.DateField(widget = DateInput()) 
    amount = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control form control-alternative'}), label="plata")
    employeeID = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}), label="ID de empleado")
    dateVisit = forms.DateField(widget = DateInput())
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

class userForm(forms.ModelForm):
    class Meta:
        model = commonUserModel
        fields = ('userFirstName','userLastName','userPhoneNumber','userRut','userType','company')
        labels = {
            'userFirstName': 'Nombre',
            'userLastName': 'Apellido',
            'userPhoneNumber': 'Numero de Celular',
            'userRut': 'Rut',
            'userType': 'Tipo Usuario',
            'company': 'Compania'
        }
        widgets = {
            'userFirstName': forms.TextInput(attrs={'class': 'form-control form control-alternative', 'id':'fn'}),
            'userLastName': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
            'userPhoneNumber': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
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

RESPONSABLES_CHOICES = []

try:
    responsables = commonUserModel.get_responsables()
    for res in responsables:
        RESPONSABLES_CHOICES.append(tuple((getattr(res, 'id'), getattr(res, 'userFirstName'))))
except:
    print("No hay usuarios responsables aun")

class companyForm(forms.ModelForm):
    class Meta:
        model = company
        fields = ('name','description','responsable', 'userAddress')
        labels = {
            'name': 'Nombre',
            'description': 'Descripcion',
            'responsable': 'Responsable',
            'userAddress': 'Direccion'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form control-alternative', 'id':'fn'}),
            'description': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
            'responsable': forms.Select(attrs={'class': 'form-control form control-alternative'}, choices=RESPONSABLES_CHOICES),
            'userAddress': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
        }