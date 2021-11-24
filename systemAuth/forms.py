from django.contrib.auth.models import User
from django import forms

from .models import commonUserModel, company , training , order
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

class DateWidget(forms.DateInput):
    input_type = 'date'

#class orderForm(forms.Form):
class orderForm(forms.ModelForm):
    class Meta:
        model = order
        fields = ('userID','type','nextPayment','amount','employeeID','dateVisit','description','improvement')
        labels = {
            'userID':  'ID usuario',
            'type': 'Tipo de Orden',
            'nextPayment': 'Siguiente fecha de pago',
            'amount': 'Monto a pagar',
            'employeeID': 'Profesional Asignado',
            'dateVisit': 'Fecha visita',
            'description': 'Descripcion',
            'improvement': 'Mejora',
        }
        widgets = {
         'userID':  forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
         'type': forms.Select(attrs={'class': 'btn btn-secondary dropdown-toggle'}) ,
         'nextPayment':DateWidget(),
         'amount': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
         'employeeID':forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
         'dateVisit': DateWidget(),
         'description': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
         'improvement': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
        }

    # userID = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}), label="ID de usuario")
    # orderType = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}), label="Tipo de orden")
    # nextPayment = forms.DateField(widget = DateInput()) 
    # amount = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control form control-alternative'}), label="plata")
    # employeeID = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}), label="ID de empleado")
    # dateVisit = forms.DateField(widget = DateInput())
    # orderDescription = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}), label="orden description")
    # improvement = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}), label="orden description")

    
    

class userForm(forms.ModelForm):
    class Meta:
        model = commonUserModel
        fields = ('firstName','lastName','phoneNumber','rut','userType','company')
        labels = {
            'firstName': 'Nombre',
            'lastName': 'Apellido',
            'phoneNumber': 'Numero de Celular',
            'rut': 'Rut',
            'userType': 'Tipo Usuario',
            'company': 'Compania'
        }
        widgets = {
            'firstName': forms.TextInput(attrs={'class': 'form-control form control-alternative', 'id':'fn'}),
            'lastName': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
            'rut': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
            'userType': forms.Select(attrs={'class': 'btn btn-secondary dropdown-toggle'}),
            'company': forms.Select(attrs={'class': 'btn btn-secondary dropdown-toggle'}),
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



class companyForm(forms.ModelForm):
    class Meta:
        model = company
        fields = ('name','description', 'address')
        labels = {
            'name': 'Nombre',
            'description': 'Descripcion',
          #  'responsable': 'Responsable',
            'address': 'Direccion'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form control-alternative', 'id':'fn'}),
            'description': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
         #   'responsable': forms.Select(attrs={'class': 'form-control form control-alternative'}, choices=RESPONSABLES_CHOICES),
            'address': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
        }

RESPONSABLES_CHOICES = []

try:
    responsables = commonUserModel.get_responsables()
    for res in responsables:
        RESPONSABLES_CHOICES.append(tuple((getattr(res, 'id'), getattr(res, 'firstName') +' '+ getattr(res, 'lastName'))))
except:
    print("No hay usuarios responsables aun")

CLIENT_CHOICES = []

try:
    responsables = commonUserModel.get_clients()
    for res in responsables:
        CLIENT_CHOICES.append(tuple((getattr(res, 'id'), getattr(res, 'firstName') +' '+ getattr(res, 'lastName'))))
except:
    print("No hay usuarios clientes aun")

class trainingForm(forms.ModelForm):
    class Meta:
        model = training
        fields = ('name','professionalAssigned','client1','client2','client3','date')
        labels = {
            'name': 'Nombre Capacitacion',
            'professionalAssigned': 'Profesional Asignado',
            'client1': 'Cliente 1',
            'client2': 'Cliente 2',
            'client3': 'Cliente 3',
            'date': 'Fecha Capacitacion',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form control-alternative'}),
            'professionalAssigned': forms.Select(attrs={'class': 'form-control form control-alternative'}, choices=RESPONSABLES_CHOICES),
            'client1': forms.Select(attrs={'class': 'form-control form control-alternative'}, choices=CLIENT_CHOICES),
            'client2': forms.Select(attrs={'class': 'form-control form control-alternative'}, choices=CLIENT_CHOICES),
            'client3': forms.Select(attrs={'class': 'form-control form control-alternative'}, choices=CLIENT_CHOICES),
            'date': forms.DateInput(),
        }