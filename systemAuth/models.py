from django.db import models
from django.contrib.auth.models import User

CLIENT_TYPES = ((0, 'Cliente' ),
                (1, 'Profesional'),
                (2, 'Admin' ))

class commonUserModel(models.Model):
  
  user = models.OneToOneField(User, on_delete = models.CASCADE, related_name="extend")
  company = models.ForeignKey('company', on_delete = models.CASCADE)
  userFirstName = models.CharField(max_length=30)
  userLastName = models.CharField(max_length=30)
  userPhoneNumber = models.CharField(max_length=20)
  userRut = models.CharField(max_length=20, unique= True)
  userType = models.IntegerField(choices=CLIENT_TYPES, default=1)
  disabled = models.BooleanField(default = False)
  
  def __str__(self):
      return self.userRut

  def getUserExtended(userID):
      return commonUserModel.objects.get(id = userID)

  def get_responsables():
      return commonUserModel.objects.filter(userType = 1)
    


class company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    responsable = models.IntegerField()
    userAddress = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_all_companies():
        return company.objects.all()
    
    def get_company(id):
        return company.objects.get(id=id)

        
        
