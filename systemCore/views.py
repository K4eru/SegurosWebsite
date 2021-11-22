from django.forms.forms import Form
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from systemAuth.forms import orderForm 
from systemAuth.models import commonUserModel
from django.contrib.auth.models import User
import requests, json
# Create your views here.
	
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
	context['order'] = orderForm(initial={'userID': 500})
	context['userExtend'] = commonUserModel.getUserExtended(request.user.id)
	
	return render(request=request, template_name="submit-order.html",context=context)	
	


def register_order(request):  #cambiar nombre vista
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
	context['order'] = orderForm(initial={'userID': 500})
	context['userExtend'] = commonUserModel.getUserExtended(request.user.id)
	
	return render(request=request, template_name="profile.html",context=context)	