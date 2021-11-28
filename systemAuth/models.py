from django.db import models
from django.contrib.auth.models import User

CLIENT_TYPES = ((0, 'Cliente' ),
                (1, 'Profesional'),
                (2, 'Admin' ))

ORDER_TYPES = ((0, 'Normal' ),
                (1, 'Especial'))

class commonUserModel(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name="extend")
    company = models.ForeignKey('company', on_delete = models.CASCADE)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    phoneNumber = models.CharField(max_length=20)
    rut = models.CharField(max_length=20, unique= True)
    userType = models.IntegerField(choices=CLIENT_TYPES, default=1)
    disabled = models.BooleanField(default = False)
    
    def __str__(self):
        return self.rut

    def getUserExtended(userID):
        return commonUserModel.objects.get(id = userID)

    def get_responsables():
        return commonUserModel.objects.filter(userType = 1)
    
    def get_clients():
        return commonUserModel.objects.filter(userType = 0)
    

class company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # responsable = models.IntegerField()
    address = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_all_companies():
        return company.objects.all()
    
    def get_company(id):
        return company.objects.get(id=id)

class order(models.Model):
    userID = models.IntegerField()
    type =  models.IntegerField(choices=ORDER_TYPES, default=0)
    nextPayment = models.DateField(default='1970-01-01')
    amount = models.IntegerField(default=0)
    employeeID = models.IntegerField()
    dateVisit = models.DateField(default='1970-01-01')
    description = models.TextField(blank=True)
    improvement = models.TextField(blank=True)
    edited = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

    def get_all_orders():
        return order.objects.all()

    def get_order(id):
        return order.objects.get(id = id)

    # def getTotalAmount():
    #     return order.objects.aggregate(total=sum('amount'))


class training(models.Model):
    name=models.CharField(max_length=100)
    professionalAssigned = models.IntegerField()
    client1 = models.IntegerField()
    client2 = models.IntegerField()
    client3 = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return self.name

class checklist(models.Model):
    orderID = models.OneToOneField(order, on_delete = models.CASCADE, related_name="extend")
    title= models.CharField(max_length=100)
    professionalAssigned = models.IntegerField()
    question1 = models.CharField(max_length=100)
    answer1 = models.CharField(max_length=100)
    question2 = models.CharField(max_length=100)
    answer2 = models.CharField(max_length=100)
    question3 = models.CharField(max_length=100)
    answer3 = models.CharField(max_length=100)
    question4 = models.CharField(max_length=100)
    answer4 = models.CharField(max_length=100)
    question5 = models.CharField(max_length=100)
    answer5 = models.CharField(max_length=100)

    def __str__(self):
        return self.title