import json
from django.db.models.aggregates import Sum
from django.shortcuts import render, redirect
from systemAuth.forms import   userForm , mainUserForm #, companyForm , orderForm , trainingForm , CLIENT_CHOICES checklistForm 
from systemAuth.models import commonUserModel
from .forms import companyForm, orderForm , trainingForm , checklistForm
from .services import get_companies , get_orders, get_trainings, get_checklist, get_order , get_checklists
import requests


# Create your views here.

from django.http import FileResponse
import io 
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import re

def generatePDFGlobal(request):
	# money = re.sub('\D+','',str(order.objects.aggregate(Sum("amount"))))
	buf = io.BytesIO()

	c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

	textob = c.beginText()

	textob.setTextOrigin(inch, inch)
	textob.setFont("Times-Roman", 14)
	c.drawString(240,30,'Reporte global de sistema')

	amount = []
	for amt in get_orders():
		amount.append(amt["amount"])


	lines = []
	
	lines.append("Usuarios que utilizan el sistema: {0}".format(commonUserModel.objects.exclude(userType=2).count()))
	lines.append("")
	lines.append("Compañias registradas en nuestro sistema : {0}".format(len(get_companies())))
	lines.append("")
	lines.append("Dinero ganado : ${:,.0f}".format(int(sum(amount))))
	lines.append("")
	lines.append("")
	lines.append("                                              Informacion de Profesionales")
	lines.append("")
	lines.append("")

	professionals = commonUserModel.get_responsables()

	orders=get_orders()
	ORDER=[]

	for ord in orders:
		ORDER.append(tuple((ord["id"],ord["userID"],ord["type"],
							ord["nextPayment"],ord["amount"],ord["employeeID"],
							ord["dateVisit"],ord["description"],ord["improvement"],
							ord["edited"])))

	#CHECK EMPLOYEE LOGGED
	
	CHECKLISTS= []

	for check in get_checklists():
		CHECKLISTS.append(tuple((check["id"],check["orderID"],check["title"],check["professionalAssigned"],
								check["question1"],check["answer1"],check["question2"],check["answer2"],
								check["question3"],check["answer3"],check["question4"],check["answer4"],
								check["question5"],check["answer5"])))


	


	for prof in professionals:
		
		lines.append("############################################")
		lines.append("")
		lines.append("ID Profesional: {0}".format(prof.pk))
		lines.append("Nombre Profesional: {0} {1}".format(prof.firstName,prof.lastName))
		lines.append("Cantidad de ordenes registradas: {0}".format( len([element for element in ORDER if element[5]==prof.pk])))
		lines.append("Cantidad de Capacitaciones registradas: {0}".format(len([element for element in CHECKLISTS if element[3]==prof.pk])))
		lines.append("")

	for line in lines:
		textob.textLine(line)

	c.drawText(textob)
	c.showPage()
	c.save()
	buf.seek(0)

	return FileResponse(buf, as_attachment=True, filename= "GlobalReport.pdf")

def generatePDFClients(request):
	# money = re.sub('\D+','',str(order.objects.aggregate(Sum("amount"))))
	buf = io.BytesIO()

	c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

	textob = c.beginText()

	textob.setTextOrigin(inch, inch)
	textob.setFont("Times-Roman", 14)
	c.drawString(240,30,'Reporte global de Clientes')


	lines = []

	orders=get_orders()
	ORDER=[]

	for ord in orders:
		ORDER.append(tuple((ord["id"],ord["userID"],ord["type"],
							ord["nextPayment"],ord["amount"],ord["employeeID"],
							ord["dateVisit"],ord["description"],ord["improvement"],
							ord["edited"])))



	clients = commonUserModel.get_clients()

	for clie in clients:
		
		lines.append("############################################")
		lines.append("")
		lines.append("ID Cliente: {0}".format(clie.pk))
		lines.append("Nombre Cliente: {0} {1}".format(clie.firstName,clie.lastName))
		lines.append("Rut: {0}".format(clie.rut))
		lines.append("Numero telefono: {0}".format(clie.phoneNumber))
		lines.append("Cantidad de ordenes registradas: {0}".format( len([element for element in ORDER if element[1]==clie.pk])))
		lines.append("")

	for line in lines:
		textob.textLine(line)






	c.drawText(textob)
	c.showPage()
	c.save()
	buf.seek(0)

	return FileResponse(buf, as_attachment=True, filename= "ClientReport.pdf")


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


####################### REGISTROS##############################
def register_company(request):
	poto = get_companies()
	
	if request.user.extend.userType != 2:
		return redirect('request_login')
		
	if request.method == "POST":
		if "registerCompany" in request.POST:
			form = companyForm(request.POST)
			if form.is_valid():
				url = 'http://127.0.0.1:8001/api/company/'
			
				payload = { 'name' : form.cleaned_data["name"] ,
							'description' : form.cleaned_data["description"] , 
							'address' : form.cleaned_data["address"] } 
				
							
				r = requests.post(url,data= payload)
			
			return redirect('registerCompany')
		else:
			return redirect('registerCompany')

	context = {}
	context['form'] = companyForm
	context['userExtend'] = commonUserModel.getUserExtended(request.user.id)
	return render(request, template_name='auth/registerCompany.html', context= context)

def submit_Order(request):
	if request.method == "POST":
		if "registerOrder" in request.POST:
			form = orderForm(request.POST)
			if form.is_valid():
				url = 'http://127.0.0.1:8001/api/order/'
				payload = { 'userID' : form.cleaned_data["userID"] ,
						    'type' : form.cleaned_data["type"] , 
							'nextPayment' : form.cleaned_data['nextPayment'] ,
							'amount' : form.cleaned_data["amount"] , 
							'employeeID' : form.cleaned_data["employeeID"] ,
							'dateVisit' : form.cleaned_data['dateVisit'] , 
							'description' : form.cleaned_data["description"],
							'improvement' : form.cleaned_data["improvement"],
							'edited': form.cleaned_data["edited"]}
							
							
				r = requests.post(url,data= payload)
				
				return redirect('order')
			else:
				print("no paso")
				return redirect('order')
	context = {}
	context['order'] = orderForm(initial={'userID': request.user.id})
	
	return render(request=request, template_name="submit-order.html",context=context)	

def submit_training(request):
	if request.method == "POST":
		if "registerTraining" in request.POST:
			form = trainingForm(request.POST)
			if form.is_valid():
				url = 'http://127.0.0.1:8001/api/training/'
				payload = { 'name' : form.cleaned_data["name"] ,
						    'professionalAssigned' : form.cleaned_data["professionalAssigned"] , 
							'client1' : form.cleaned_data['client1'] ,
							'client2' : form.cleaned_data["client2"] , 
							'client3' : form.cleaned_data["client3"] ,
							'date' : form.cleaned_data['date'] 
							}
													
				r = requests.post(url,data= payload)
				

				return redirect('submit-training')
			else:
				
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
				url = 'http://127.0.0.1:8001/api/checklist/'
				payload = { 'orderID' : form.cleaned_data["orderID"] ,
						    'title' : form.cleaned_data["title"] , 
							'professionalAssigned' : form.cleaned_data['professionalAssigned'] ,
							'question1' : form.cleaned_data["question1"] , 
							'answer1' : form.cleaned_data["answer1"] ,
							'question2' : form.cleaned_data["question2"] ,
							'answer2' : form.cleaned_data["answer2"] ,
							'question3' : form.cleaned_data["question3"] ,
							'answer3' : form.cleaned_data["answer3"] ,
							'question4' : form.cleaned_data["question4"] ,
							'answer4' : form.cleaned_data["answer4"] ,
							'question5' : form.cleaned_data["question5"] ,
							'answer5' : form.cleaned_data["answer5"] 							 
							}
													
				r = requests.post(url,data= payload)

				return redirect('submit_checklist')
			else:
				
				return redirect('submit_checklist')

	context = {}
	context['form'] = checklistForm(initial={'professionalAssigned': request.user.id})
	return render(request=request, template_name="submit-checklist.html", context=context)


####################### SHOW INFO ##############################

def show_clientPayment(request):

	orders=get_orders()
	ORDER=[]

	for ord in orders:
		ORDER.append(tuple((ord["id"],ord["userID"],ord["type"],
							ord["nextPayment"],ord["amount"],ord["employeeID"],
							ord["dateVisit"],ord["description"],ord["improvement"],
							ord["edited"])))
	res = []

	for i in ORDER:
		val = list(i)
		clientInstance = commonUserModel.getUserExtended(val[1])
		val[1] = clientInstance.firstName+' '+clientInstance.lastName

		res.append(tuple(val))

			
	context={}
	context['queryset'] = res

	return render(request,template_name="show-client-payment.html",context=context)

def show_order(request):
	idUser = request.user.id
	
	orders=get_orders()
	ORDER=[]

	for ord in orders:
		ORDER.append(tuple((ord["id"],ord["userID"],ord["type"],
							ord["nextPayment"],ord["amount"],ord["employeeID"],
							ord["dateVisit"],ord["description"],ord["improvement"],
							ord["edited"])))

	#CHECK EMPLOYEE LOGGED
	orderList = [element for element in ORDER if element[5]==idUser]
	
	if not orderList:
		#CLIENT LOGGED
		orderList = [element for element in ORDER if element[1]==idUser]
	
	res = []

	for i in orderList:
		val = list(i)
		clientInstance = commonUserModel.getUserExtended(val[1])
		val[1] = clientInstance.firstName+' '+clientInstance.lastName

		profInstance = commonUserModel.getUserExtended(val[5])
		val[5] = profInstance.firstName+' '+profInstance.lastName
		
		res.append(tuple(val))

	context={}
	context['queryset'] = res

	return render(request,template_name="show-orders.html", context= context)


def show_training(request):
	listTraining = get_trainings()	

	TRAININGS = []

	for tra in listTraining:
		TRAININGS.append(tuple((tra["id"],tra["name"],tra["professionalAssigned"],
								tra["client1"],tra["client2"],tra["client3"],tra["date"])))

	res =[]

	for i in TRAININGS:
		val = list(i)
		professionalInstance = commonUserModel.getUserExtended(val[2])
		val[2] = professionalInstance.firstName+' '+professionalInstance.lastName

		client1Instance = commonUserModel.getUserExtended(val[3])
		val[3] = client1Instance.firstName+' '+client1Instance.lastName

		client2nstance = commonUserModel.getUserExtended(val[4])
		val[4] = client2nstance.firstName+' '+client2nstance.lastName

		client3Instance = commonUserModel.getUserExtended(val[5])
		val[5] = client3Instance.firstName+' '+client3Instance.lastName

		res.append(tuple(val))

	context={}
	context['queryset'] = res

	return render(request,template_name="show-trainings.html", context= context)

def show_checklist(request):
	idUser = request.user.id
	listchecklist = get_checklists()
	
	CHECKLISTS= []

	for check in listchecklist:
		CHECKLISTS.append(tuple((check["id"],check["orderID"],check["title"],check["professionalAssigned"],
								check["question1"],check["answer1"],check["question2"],check["answer2"],
								check["question3"],check["answer3"],check["question4"],check["answer4"],
								check["question5"],check["answer5"])))

	print(CHECKLISTS)
	# FILTER
	checklistAux = [element for element in CHECKLISTS if element[3]==idUser]

	res = []
	
	for i in checklistAux:
		val = list(i)
		profInstance = commonUserModel.getUserExtended(val[3])
		val[3] = profInstance.firstName+' '+profInstance.lastName

		res.append(tuple(val))

	context={}
	context['queryset'] = res

	return render(request,template_name="show-checklist.html",context=context)

#####################   EDIT INFO  #############################

def update_order(request,order_pk): 

	orders = get_order(order_pk)

	# ORDERS = []
	# for orde in orders:
	# 	ORDERS.append(tuple((orde["userID"],orde["type"],orde["nextPayment"],
	# 						orde["amount"],orde["employeeID"],orde["dateVisit"],orde["description"],
	# 						orde["improvement"],orde["edited"])))
        
	# orderAUX = [element for element in ORDERS if element[0]==id]
	
	extendedInstance = orders
	print(extendedInstance["nextPayment"])
	#print(extendedInstance)
	initExtend = {'userID': extendedInstance["userID"],
				  'type': extendedInstance["type"],
				  'nextPayment': extendedInstance["nextPayment"],
				  'amount': extendedInstance["amount"],
				  'employeeID' : extendedInstance["employeeID"],
				  'dateVisit': extendedInstance["dateVisit"],
				  'description': extendedInstance["description"],
				  'improvement': extendedInstance["improvement"],
				  'edited': 1
	}
	print(initExtend)
	if request.method == "POST":
		if "editOrder" in request.POST:
			form = orderForm(request.POST)
			
			if form.is_valid() :
				print(form.cleaned_data['nextPayment'])
				payload = { 'userID' : form.cleaned_data["userID"] ,
						    'type' : form.cleaned_data["type"] , 
							'nextPayment' : str(form.cleaned_data["nextPayment"]) ,
							'amount' : form.cleaned_data["amount"] , 
							'employeeID' : form.cleaned_data["employeeID"] ,
							'dateVisit' : str(form.cleaned_data["dateVisit"]) , 
							'description' : form.cleaned_data["description"],
							'improvement' : form.cleaned_data["improvement"],
							'edited': '1'}

				url = 'http://127.0.0.1:8001/api/order/{0}/'.format(order_pk)
				r = requests.patch(url=url,json=payload)
				print(r.status_code)
				return redirect('show_order')
			else:
				
				return redirect('show_order')

	context = {}
	context['order'] = orderForm(initial=initExtend)


	return render(request=request, template_name="edit-order.html", context= context)	

def update_checklist(request,checklist_pk): 

	checklists = get_checklist(checklist_pk)
	extendedInstance = checklists

	initExtend = {'orderID': extendedInstance["orderID"],
				  'title': extendedInstance["title"],
				  'professionalAssigned': extendedInstance["professionalAssigned"],
				  'question1': extendedInstance["question1"] ,
				  'answer1' : extendedInstance["answer1"],
				  'question2': extendedInstance["question2"],
				  'answer2': extendedInstance["answer2"],
				  'question3': extendedInstance["question3"],
				  'answer3': extendedInstance["answer3"],
				  'question4': extendedInstance["question4"],
				  'answer4': extendedInstance["answer4"],
				  'question5': extendedInstance["question5"],
				  'answer5': extendedInstance["answer5"]
	}
	if request.method == "POST":
		if "editChecklist" in request.POST:
			form = checklistForm(request.POST)
			if form.is_valid() :
				payload = {'orderID': form.cleaned_data["orderID"],
				  			'title': form.cleaned_data["title"],
				  			'professionalAssigned': form.cleaned_data["professionalAssigned"],
				  			'question1': form.cleaned_data["question1"] ,
				  			'answer1' : form.cleaned_data["answer1"],
				  			'question2': form.cleaned_data["question2"],
				  			'answer2': form.cleaned_data["answer2"],
				  			'question3': form.cleaned_data["question3"],
				  			'answer3': form.cleaned_data["answer3"],
				  			'question4': form.cleaned_data["question4"],
				  			'answer4': form.cleaned_data["answer4"],
				  			'question5': form.cleaned_data["question5"],
				  			'answer5': form.cleaned_data["answer5"]}

				url = 'http://127.0.0.1:8001/api/checklist/{0}/'.format(checklist_pk)
				r = requests.patch(url=url,json=payload)
				print(r.status_code)			  


				return redirect('show_checklist')
			else:
				
				return redirect('show_checklist')

	context = {}
	context['form'] = checklistForm(initial=initExtend)


	return render(request=request, template_name="edit-checklist.html", context= context)	
