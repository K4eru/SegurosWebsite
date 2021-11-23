from django.contrib.auth.forms import UserModel
from django.forms.forms import Form
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from systemAuth import models
from django.contrib import messages
from systemAuth.forms import orderForm , userForm , mainUserForm , trainingForm
from systemAuth.models import commonUserModel, training
from django.contrib.auth.models import User
import requests, json
# Create your views here.
	

def update_profile(request):  #cambiar nombre vista

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
				url = 'http://127.0.0.1:8001/api/order/'
				payload = { 'userID' : form.cleaned_data["userID"] ,
						    'orderType' : form.cleaned_data["orderType"] , 
							#'nextPayment' : form.cleaned_data('nextPayment') ,
							'amount' : form.cleaned_data["amount"] , 
							'employeeID' : form.cleaned_data["employeeID"] ,
						#	'dateVisit' : form.cleaned_data('dateVisit') , 
							'orderDescription' : form.cleaned_data["orderDescription"]}
			
				r = requests.post(url,data= payload)
				return redirect('profile_details')
			else:
				
				return redirect('profile_details')
	print(request.user.id)
	context = {}
	context['order'] = orderForm(initial={'userID': request.user.id})
	context['userExtend'] = commonUserModel.getUserExtended(request.user.id)
	
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
	context['form'] = trainingForm
	context['userExtend'] = commonUserModel.getUserExtended(request.user.id)
	return render(request=request, template_name="submit-training.html", context=context)