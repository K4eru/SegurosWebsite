from django.contrib.auth.forms import UserCreationForm
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
    username = forms.EmailInput()
    class Meta:
        models = userForm
        fields = ['username']
        labels = {
            'username': 'Correo',
        } 
    def init(self, args, **kwargs):
        super(mainUserForm, self).init(args, **kwargs)
 




#class UserLoginForm(AuthenticationForm):
#    def __init__(self, *args, **kwargs):
#        super(UserLoginForm, self).__init__(*args, **kwargs)

#    username = forms.CharField(widget=forms.TextInput(
#        attrs={'class': 'form-control', 'placeholder': 'Usuario', 'id': 'hello'}))

#    password = forms.CharField(widget=forms.PasswordInput(
#        attrs={'class': 'form-control', 'placeholder': 'Contrasena', }))