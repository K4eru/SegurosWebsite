from django.contrib.auth import forms
from django.shortcuts import  render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from . import forms

def request_login(request):
	if request.method == "POST":
		form = forms.UserLoginForm(request, data=request.POST)
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
	form = forms.UserLoginForm()
	return render(request=request, template_name="auth/login.html", context={"login_form":form})

def register_user(request):
	return render(request,'auth/register.html')
