from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .services import get_companies , get_orders
from systemAuth.models import commonUserModel
import re

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

ORDER_CHOICES = []
orders = get_orders()

try:
    for res in orders:
        ORDER_CHOICES.append(tuple((res["id"],res["id"])))
except:
    print("no existen ordenes")


#WIDGET FECHAS
class DateWidget(forms.DateInput):
    input_type = 'date'


#FORM COMPANIA
class companyForm(forms.Form):
    
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}), label="Nombre Compañia")
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}), label="Descripcion")
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}), label="Direccion")


#FORM ORDEN 

class orderForm(forms.Form):
    for aux in CLIENT_CHOICES:
        if(re.match("\([\d,\s]+\)",str(aux))):
            CLIENT_CHOICES.remove(aux)
        
    for aux in RESPONSABLES_CHOICES:
        if(re.match("\([\d,\s]+\)",str(aux))):
            RESPONSABLES_CHOICES.remove(aux)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nextPayment'].initial = '1970-01-01'
        self.fields['amount'].initial = 0
        self.fields['dateVisit'].initial = '1970-01-01'
        self.fields['improvement'].initial = '--'
        self.fields['edited'].initial = 0
        self.fields['description'].initial = ''
        
    userID = forms.IntegerField(widget=forms.Select(attrs={'class': 'form-control form control-alternative'},choices=CLIENT_CHOICES), label="ID Usuario")
    type= forms.IntegerField(widget=forms.Select(attrs={'class': 'form-control form control-alternative'},choices=ORDER_TYPES), label="Tipo orden")
    nextPayment = forms.DateField(widget=(DateWidget()), initial='1970-01-01')
    amount = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}), label="Monto", initial="0")
    employeeID = forms.IntegerField(widget=forms.Select(attrs={'class': 'form-control form control-alternative'}, choices=RESPONSABLES_CHOICES), label="Profesional")
    dateVisit = forms.DateField(widget=(DateWidget()), initial='1970-01-01')
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}), label="Descripcion",initial="")
    improvement = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}), label="Mejora",initial="")
    edited = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}), label="Edited", initial="0")

class trainingForm(forms.Form):
    for aux in CLIENT_CHOICES:
        if(re.match("\([\d,\s]+\)",str(aux))):
            CLIENT_CHOICES.remove(aux)
        
    for aux in RESPONSABLES_CHOICES:
        if(re.match("\([\d,\s]+\)",str(aux))):
            RESPONSABLES_CHOICES.remove(aux)
    
    name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}),label="Nombre Capacitacion")
    professionalAssigned = forms.IntegerField(widget=forms.Select(attrs={'class': 'form-control form control-alternative'}, choices=RESPONSABLES_CHOICES))
    client1 = forms.IntegerField(widget=forms.Select(attrs={'class': 'form-control form control-alternative'}, choices=CLIENT_CHOICES))
    client2 = forms.IntegerField(widget=forms.Select(attrs={'class': 'form-control form control-alternative'}, choices=CLIENT_CHOICES))
    client3 = forms.IntegerField(widget=forms.Select(attrs={'class': 'form-control form control-alternative'}, choices=CLIENT_CHOICES))
    date= forms.DateField(widget=(DateWidget()))


class checklistForm(forms.Form):
    for aux in RESPONSABLES_CHOICES:
        if(re.match("\([\d,\s]+\)",str(aux))):
            RESPONSABLES_CHOICES.remove(aux)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['answer1'].initial = '--'
        self.fields['answer2'].initial = '--'
        self.fields['answer3'].initial = '--'
        self.fields['answer4'].initial = '--'
        self.fields['answer5'].initial = '--'

    orderID=forms.IntegerField(widget=forms.Select(attrs={'class': 'form-control form control-alternative'}, choices=ORDER_CHOICES))
    title=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}))
    professionalAssigned=forms.IntegerField(widget=forms.Select(attrs={'class': 'form-control form control-alternative'}, choices=RESPONSABLES_CHOICES))
    question1=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}))
    answer1=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}))
    question2=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}))
    answer2=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}))
    question3=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}))
    answer3=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}))
    question4=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}))
    answer4=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}))
    question5=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}))
    answer5=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form control-alternative'}))
