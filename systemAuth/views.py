from django.db.models.aggregates import Count, Sum
from django.shortcuts import  render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import  mainUserForm, userForm, UserLoginForm  
from systemCore.services import get_companies,get_orders, get_trainings
from systemAuth.models import  commonUserModel 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from collections import Counter
import requests

@login_required(login_url='request_login')
def home(request):
	
	context = {}
	#DATA FOR ADDONS IN ADMIN INDEX LUL
	context['userExtend'] = commonUserModel.getUserExtended(request.user.id)
	context['totalUsers'] = commonUserModel.objects.count()
	context['totalOrders'] = len(get_orders())

	context['totalCompanys'] = len(get_companies())
	orders = get_orders()
	amount = []
	for amt in orders:
		amount.append(amt["amount"])

	context['moneyEarned'] = sum(amount)


	#DATA FOR GRAPHICS LUL
	companies = get_companies()

	clientlist = commonUserModel.get_clients()
	clientOrders = []
	clientName = []
	
	for client in clientlist:
		clientOrders.append(len([element for element in orders if element["userID"]==client.id]))
		clientName.append("{0} {1}".format(client.firstName,client.lastName))
		
	companyNames =[]
	companyCount = []
	for aux in companies:
		companyNames.append(aux["name"])
		#print([element for element in companies if element["id"]==aux["id"]])
		companyCount.append(commonUserModel.objects.filter(company=aux["id"]).count())

	context['companyNames'] = companyNames
	context['companyCount'] = companyCount
	context['clientOrders'] = clientOrders
	context['clientNames'] = clientName

    #DATA FOR PROFESSIONAL HEHE
	ORDER=[]

	for ord in orders:
		ORDER.append(tuple((ord["id"],ord["userID"],ord["type"],
							ord["nextPayment"],ord["amount"],ord["employeeID"],
							ord["dateVisit"],ord["description"],ord["improvement"],
							ord["edited"])))

	orderList = [element for element in ORDER if element[5]==request.user.id]

	context['ordersAssigned'] = orderList

	TRAININGS = []

	listTraining = get_trainings()
	for tra in listTraining:
		TRAININGS.append(tuple((tra["id"],tra["name"],tra["professionalAssigned"],
								tra["client1"],tra["client2"],tra["client3"],tra["date"])))

	trainingList = [element for element in TRAININGS if element[2]==request.user.id]

	context['trainingAssigned'] = trainingList

	#DATA FOR CLIENT LMAO
	ORDERCLIENT=[]

	for ord in orders:
		ORDERCLIENT.append(tuple((ord["id"],ord["userID"],ord["type"],
							ord["nextPayment"],ord["amount"],ord["employeeID"],
							ord["dateVisit"],ord["description"],ord["improvement"],
							ord["edited"])))

	orderClientList = [element for element in ORDERCLIENT if element[0]==request.user.id]

	RESS = []

	for aux in orderClientList:
		profInstance = commonUserModel.getUserExtended(aux[5])
		RESS.append(tuple((aux[0],profInstance.firstName+' '+profInstance.lastName,aux[9])))
	 	
	print(RESS)
	
	context['clientAssignedOrder'] = RESS
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

				userextended = commonUserModel(user = user, firstName = form.cleaned_data['firstName'], lastName = form.cleaned_data['lastName'], 
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



		
