from django.contrib.auth.forms import UserModel
from django.forms.forms import Form
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from systemAuth import models
from django.contrib import messages
from systemAuth.forms import  checklistForm, orderForm , userForm , mainUserForm , trainingForm
from systemAuth.models import checklist, commonUserModel, training , order
from django.contrib.auth.models import User
import requests, json
# Create your views here.

def show_training(request):
	userID = request.user.id
	listTraining = training.objects.all()
	
	

	for train in listTraining:
		professionalInstance = commonUserModel.getUserExtended(train.professionalAssigned)
		train.professionalName = professionalInstance.firstName+' '+professionalInstance.lastName

		client1Instance = commonUserModel.getUserExtended(train.client1)
		train.client1 = client1Instance.firstName+' '+client1Instance.lastName

		client2nstance = commonUserModel.getUserExtended(train.client2)
		train.client2 = client2nstance.firstName+' '+client2nstance.lastName

		client3Instance = commonUserModel.getUserExtended(train.client3)
		train.client3 = client3Instance.firstName+' '+client3Instance.lastName


	context={}
	context['queryset'] = listTraining

	return render(request,template_name="show-trainings.html", context= context)

def show_order(request):
	idUser = request.user.id
	listOrder = order.objects.filter(employeeID = idUser)
	if not listOrder:
		listOrder = order.objects.filter(userID = idUser)

	for aux in listOrder:
		profInstance = commonUserModel.getUserExtended(aux.employeeID)
		aux.employeeID = profInstance.firstName+' '+profInstance.lastName

		userInstance = commonUserModel.getUserExtended(aux.userID)
		aux.userID = userInstance.firstName+' '+userInstance.lastName

	context={}
	context['queryset'] = listOrder

	return render(request,template_name="show-orders.html", context= context)

def update_order(request,order_pk): 

	id = order_pk
	extendedInstance = order.get_order(id)

	initExtend = {'userID': extendedInstance.userID,
				  'type': extendedInstance.type,
				  'nextPayment': extendedInstance.nextPayment,
				  'amount': extendedInstance.amount ,
				  'employeeID' : extendedInstance.employeeID,
				  'dateVisit': extendedInstance.dateVisit,
				  'description': extendedInstance.description,
				  'improvement': extendedInstance.improvement,
				  'edited': extendedInstance.edited
	}
	if request.method == "POST":
		if "editOrder" in request.POST:
			form = orderForm(request.POST, instance=extendedInstance)
			if form.is_valid() :
				form.fields['userID'].disabled = True
				form.save()

				return redirect('show_order')
			else:
				
				return redirect('show_order')

	context = {}
	context['order'] = orderForm(initial=initExtend)


	return render(request=request, template_name="edit-order.html", context= context)	



def update_profile(request): 

	userID = request.user.id
	extendedInstance = commonUserModel.getUserExtended(userID)

	initExtend = {'firstName': extendedInstance.firstName,
				  'lastName': extendedInstance.lastName,
				  'phoneNumber': extendedInstance.phoneNumber,
				  'rut': extendedInstance.rut ,
				  'userType' : extendedInstance.userType,
				  'company': extendedInstance.company
	}
	if request.method == "POST":
		if "editProfile" in request.POST:
			mainForm = mainUserForm(request.POST)
			form = userForm(request.POST, instance=extendedInstance)
			if form.is_valid() :
				form.fields['rut'].disabled = True
				form.save()

				return redirect('profile_details')
			else:
				
				return redirect('profile_details')

	context = {}
	# context['form'] = orderForm()

	context['mainForm'] = userForm(initial=initExtend)

	return render(request=request, template_name="profile.html",context=context)	


def submit_Order(request):
	if request.method == "POST":
		if "registerOrder" in request.POST:
			form = orderForm(request.POST)
			if form.is_valid():
				order = models.order(userID=form.cleaned_data['userID'],type=form.cleaned_data['type'],nextPayment=form.cleaned_data['nextPayment'],amount=form.cleaned_data['amount'],employeeID=form.cleaned_data['employeeID'],dateVisit=form.cleaned_data['dateVisit'],description=form.cleaned_data['description'],improvement=form.cleaned_data['improvement'],edited=form.cleaned_data['edited'])
				order.save()
				# url = 'http://127.0.0.1:8001/api/order/'
				# payload = { 'userID' : form.cleaned_data["userID"] ,
				# 		    'orderType' : form.cleaned_data["orderType"] , 
				# 			#'nextPayment' : form.cleaned_data('nextPayment') ,
				# 			'amount' : form.cleaned_data["amount"] , 
				# 			'employeeID' : form.cleaned_data["employeeID"] ,
				# 		#	'dateVisit' : form.cleaned_data('dateVisit') , 
				# 			'orderDescription' : form.cleaned_data["orderDescription"],
				# 			'improvement' : form.cleaned_data["improvement"]}
							
				# r = requests.post(url,data= payload)
				messages.success(request , "La orden se creo exitosamente")
				return redirect('order')
			else:
				messages.error(request, "La orden no se pudo crear")
				return redirect('order')
	print(request.user.id)
	context = {}
	context['order'] = orderForm(initial={'userID': request.user.id})
	#context['userExtend'] = commonUserModel.getUserExtended(request.user.id)
	
	return render(request=request, template_name="submit-order.html",context=context)	
	

def submit_training(request):
	if request.method == "POST":
		if "registerTraining" in request.POST:
			form = trainingForm(request.POST)
			if form.is_valid():
				training = models.training(name=form.cleaned_data['name'],professionalAssigned=form.cleaned_data['professionalAssigned'],client1=form.cleaned_data['client1'],client2=form.cleaned_data['client2'],client3=form.cleaned_data['client3'],date=form.cleaned_data['date'])
				training.save()
				messages.success(request , "La capacitacion se creo exitosamente")
				return redirect('submit-training')
			else:
				messages.error(request, "La capacitacionno se pudo crear")
				return redirect('submit-training')

	context = {}
	context['form'] = trainingForm(initial={'professionalAssigned': request.user.id})
	context['userExtend'] = commonUserModel.getUserExtended(request.user.id)
	return render(request=request, template_name="submit-training.html", context=context)

def submit_checklist(request):
	if request.method == "POST":
		if "registerChecklist" in request.POST:
			form = checklistForm(request.POST)
			if form.is_valid():
				checklist = models.checklist(orderID=form.cleaned_data['orderID'],title=form.cleaned_data['title'],professionalAssigned=form.cleaned_data['professionalAssigned'],
				question1=form.cleaned_data['question1'],answer1=form.cleaned_data['answer1'],
				question2=form.cleaned_data['question2'],answer2=form.cleaned_data['answer2'],
				question3=form.cleaned_data['question3'],answer3=form.cleaned_data['answer3'],
				question4=form.cleaned_data['question4'],answer4=form.cleaned_data['answer4'],
				question5=form.cleaned_data['question5'],answer5=form.cleaned_data['answer5'])
				checklist.save()
				messages.success(request , "El checklist se creo exitosamente")
				return redirect('submit_checklist')
			else:
				messages.error(request, "El checklist no se pudo crear")
				return redirect('submit_checklist')

	context = {}
	context['form'] = checklistForm(initial={'professionalAssigned': request.user.id})
	return render(request=request, template_name="submit-checklist.html", context=context)


def show_checklist(request):
	idUser = request.user.id
	listchecklist = checklist.objects.filter(professionalAssigned = idUser)
	
	for aux in listchecklist:
		profInstance = commonUserModel.getUserExtended(aux.professionalAssigned)
		aux.professionalAssigned = profInstance.firstName+' '+profInstance.lastName


	context={}
	context['queryset'] = listchecklist

	return render(request,template_name="show-checklist.html",context=context)


def show_clientPayment(request):

	listOrder = order.get_all_orders()

	for aux in listOrder:

		userInstance = commonUserModel.getUserExtended(aux.userID)
		aux.userID = userInstance.firstName+' '+userInstance.lastName

	context={}
	context['queryset'] = listOrder

	return render(request,template_name="show-client-payment.html",context=context)