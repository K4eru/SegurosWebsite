from django.db import models
from django.contrib.auth.models import User
from systemCore.services import get_companies

CLIENT_TYPES = ((0, 'Cliente' ),
                (1, 'Profesional'),
                (2, 'Admin' ))

ORDER_TYPES = ((0, 'Normal' ),
                (1, 'Especial'))

class commonUserModel(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name="extend")
    company = models.IntegerField()
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    phoneNumber = models.CharField(max_length=20)
    rut = models.CharField(max_length=20, unique= True)
    userType = models.IntegerField(choices=CLIENT_TYPES, default=1)
    disabled = models.BooleanField(default = False)
    
    def __str__(self):
        return "{0} {1}".format(self.firstName,self.lastName)

    def getUserExtended(userID):
        return commonUserModel.objects.get(id = userID)

    def get_responsables():
        return commonUserModel.objects.filter(userType = 1)
    
    def get_clients():
        return commonUserModel.objects.filter(userType = 0)

    def get_companys():
        return commonUserModel.objects.values_list('company',flat=True)

    def get_UsersNotAdmin():
        return commonUserModel.objects.exclude(userType = 2)
