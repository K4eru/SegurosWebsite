from django.contrib.auth import forms
from django.shortcuts import  render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import mainUserForm, userForm, UserLoginForm
from . import models
from django.contrib.auth.models import User

def home(request):
	return render(request, template_name= "layouts/base.html")



def request_login(request):
	if request.method == "POST":
		form = UserLoginForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"Bienvenido {username}.")
				return redirect('home')
			else:
				messages.error(request,"Contrasena o usuario incorrecto.")
		else:
			messages.error(request,"Contrasena o usuario incorrecto.")
	form = UserLoginForm()
	return render(request=request, template_name="auth/login.html", context={"login_form":form})


def register_user(request):
	if request.method == "POST":
		if "register" in request.POST:
			mainForm = mainUserForm(request.POST)
			form = userForm(request.POST)

			if mainForm.is_valid() and form.is_valid():

				user = User.objects.create_user(mainForm.cleaned_data['username'],mainForm.cleaned_data['email'],mainForm.cleaned_data['password'])
				user.save()

				userextended = models.commonUserModel(user = user, userFirstName = form.cleaned_data['userFirstName'], userLastName = form.cleaned_data['userLastName'], userAge = form.cleaned_data['userAge'], userPhoneNumber = form.cleaned_data['userPhoneNumber'], userAddress = form.cleaned_data['userAddress'], userRut = form.cleaned_data['userRut'], userType = form.cleaned_data['userType'])
				userextended.save()

				messages.success(request , "El usuario se creo exitosamente")
				
				return redirect('request_register')
			else:
				messages.error(request, "El usuario no se pudo crear")
				return redirect('request_register')
	
	context = {}
	context['mainForm'] = mainUserForm
	context['form'] = userForm(initial={})

	return render(request, template_name='auth/register.html', context= context)
		
