from django.db import models
from django.contrib.auth.models import User

CLIENT_TYPES = ((0, 'Cliente' ),
                (1, 'Profesional'),
                (2, 'Admin' ))

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



class training(models.Model):
    name=models.CharField(max_length=100)
    professionalAssigned = models.IntegerField()
    client1 = models.IntegerField()
    client2 = models.IntegerField()
    client3 = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return self.name