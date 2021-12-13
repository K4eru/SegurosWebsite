from django.contrib.auth import forms
from django.db.models.aggregates import Count, Sum
from django.shortcuts import  render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import  mainUserForm, userForm, UserLoginForm  
from systemCore.services import get_companies
from . import models
from systemAuth.models import  commonUserModel 
from django.contrib.auth.decorators import login_required
import requests

@login_required(login_url='request_login')
def home(request):
	
	context = {}
	#DATA FOR ADDONS IN ADMIN INDEX LUL
	context['userExtend'] = commonUserModel.getUserExtended(request.user.id)
	context['totalUsers'] = commonUserModel.objects.count()
	#context['totalOrders'] = order.objects.count()
	# context['totalCompanys'] = company.objects.count()
	#context['moneyEarned'] = order.objects.aggregate(Sum("amount"))

	#DATA FOR GRAPHICS LUL
	# companies = company.objects.all()
	#companies2 = commonUserModel.get_companys()
	clientlist = commonUserModel.get_clients()
	clientOrders = []
	clientName = []
	
	for client in clientlist:
		#clientOrders.append(order.objects.filter(userID=client.user.id).count())
		clientName.append("{0} {1} - {2}".format(client.firstName,client.lastName, client.company))
	
	
	# companyNames =[]
	# companyCount = []
	# for aux in companies:
	# 	companyNames.append(aux.name)
	# 	companyCount.append(commonUserModel.objects.filter(company=aux.id).count())

	# context['companyNames'] = companyNames
	# context['companyCount'] = companyCount
	context['clientOrders'] = clientOrders
	context['clientNames'] = clientName

    #DATA FOR PROFESSIONAL HEHE
	#context['ordersAssigned'] = order.objects.filter(employeeID = request.user.id)
	#context['trainingAssigned'] = training.objects.filter(professionalAssigned = request.user.id)

	#DATA FOR CLIENT LMAO
	# listOrder = order.objects.filter(userID = request.user.id)
	# for aux in listOrder:
	# 	profInstance = commonUserModel.getUserExtended(aux.employeeID)
	# 	aux.employeeID = profInstance.firstName+' '+profInstance.lastName

	# context['clientAssignedOrder'] = listOrder
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
	context['form'] = userForm()
	
	context['userExtend'] = commonUserModel.getUserExtended(request.user.id)
	return render(request, template_name='auth/register.html', context= context)



		
