from django.contrib.auth import forms
from django.db.models.aggregates import Count, Sum
from django.shortcuts import  render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import companyForm, mainUserForm, userForm, UserLoginForm
from . import models
from systemAuth.models import commonUserModel , order , company
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required(login_url='request_login')
def home(request):
	
	context = {}
	context['userExtend'] = commonUserModel.getUserExtended(request.user.id)
	context['totalUsers'] = commonUserModel.objects.count()
	context['totalOrders'] = order.objects.count()
	context['totalCompanys'] = company.objects.count()
	context['moneyEarned'] = order.objects.aggregate(Sum("amount"))

	
	companies = company.objects.all()
	companies2 = commonUserModel.get_companys()
	clientlist = commonUserModel.get_clients()
	clientOrders = []
	clientName = []
	
	for client in clientlist:
		clientOrders.append(order.objects.filter(userID=client.user.id).count())
		clientName.append("{0} {1}".format(client.firstName,client.lastName))
	
	#context['ordercliente'] = clientlist
	companyNames =[]
	companyCount = []
	for aux in companies:
		companyNames.append(aux.name)
		companyCount.append(commonUserModel.objects.filter(company=aux.id).count())

	context['companyNames'] = companyNames
	context['companyCount'] = companyCount
	context['clientOrders'] = clientOrders
	context['clientNames'] = clientName




	return render(request, template_name= "index.html", context=context)



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
				if form.cleaned_data['userType'] == 2:
					user.is_superuser = True
					user.is_staff = True
				user.save()

				userextended = models.commonUserModel(user = user, firstName = form.cleaned_data['firstName'], lastName = form.cleaned_data['lastName'], 
				phoneNumber = form.cleaned_data['phoneNumber'], rut = form.cleaned_data['rut'], 
				userType = form.cleaned_data['userType'], company = form.cleaned_data['company'])
				userextended.save()

				
				
				return redirect('registerUser')
			else:
				
				return redirect('registerUser')
	
	context = {}
	context['mainForm'] = mainUserForm
	context['form'] = userForm(initial={})
	context['userExtend'] = commonUserModel.getUserExtended(request.user.id)
	return render(request, template_name='auth/register.html', context= context)


def register_company(request):
	if request.user.extend.userType != 2:
		return redirect('request_login')
		
	if request.method == "POST":
		if "registerCompany" in request.POST:
			form = companyForm(request.POST)
			if form.is_valid():
				company = models.company(name=form.cleaned_data['name'],description=form.cleaned_data['description'],address=form.cleaned_data['address'])
				company.save()
				
				return redirect('registerCompany')
			else:
				
				return redirect('registerCompany')


	context = {}
	context['form'] = companyForm
	context['userExtend'] = commonUserModel.getUserExtended(request.user.id)
	return render(request, template_name='auth/registerCompany.html', context= context)
		
