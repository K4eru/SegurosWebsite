from django.contrib.auth import forms
from django.shortcuts import  render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import companyForm, mainUserForm, userForm, UserLoginForm
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required(login_url='request_login')
def home(request):
	return render(request, template_name= "layouts/base.html")



def request_login(request):

	if request.user.is_authenticated:
		return redirect('home')

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
	if request.user.extend.userType != 2:
		return redirect('request_login')
		
	if request.method == "POST":
		if "register" in request.POST:
			mainForm = mainUserForm(request.POST)
			form = userForm(request.POST)
			if mainForm.is_valid() and form.is_valid():

				user = User.objects.create_user(mainForm.cleaned_data['username'],mainForm.cleaned_data['email'],mainForm.cleaned_data['password'])
				user.save()

				userextended = models.commonUserModel(user = user, userFirstName = form.cleaned_data['userFirstName'], userLastName = form.cleaned_data['userLastName'], 
				userPhoneNumber = form.cleaned_data['userPhoneNumber'], userRut = form.cleaned_data['userRut'], 
				userType = form.cleaned_data['userType'], company = form.cleaned_data['company'])
				userextended.save()

				messages.success(request , "El usuario se creo exitosamente")
				
				return redirect('request_login')
			else:
				messages.error(request, "El usuario no se pudo crear")
				return redirect('registerUser')
	
	context = {}
	context['mainForm'] = mainUserForm
	context['form'] = userForm(initial={})

	return render(request, template_name='auth/register.html', context= context)


def register_company(request):
	if request.user.extend.userType != 2:
		return redirect('request_login')
		
	if request.method == "POST":
		if "registerCompany" in request.POST:
			form = companyForm(request.POST)
			if form.is_valid():
				company = models.company(name=form.cleaned_data['name'],description=form.cleaned_data['description'],responsable=form.cleaned_data['responsable'],userAddress=form.cleaned_data['userAddress'])
				company.save()

	
	context = {}
	context['form'] = companyForm

	return render(request, template_name='auth/registerCompany.html', context= context)
		
