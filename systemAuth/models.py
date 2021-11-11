from django.db import models
from django.contrib.auth.models import User

CLIENT_TYPES = ((0, 'Cliente' ),
                (1, 'Profesional'))

class commonUserModel(models.Model):
  
  user = models.OneToOneField(User, on_delete = models.CASCADE, related_name="extend")
  userFirstName = models.CharField(max_length=30)
  userLastName = models.CharField(max_length=30)
  userAge = models.IntegerField()
  userPhoneNumber = models.CharField(max_length=20)
  userAddress = models.CharField(max_length=50) 
  userRut = models.CharField(max_length=20, unique= True)
  userType = models.IntegerField(choices=CLIENT_TYPES, default=1)
  userIsFired = models.IntegerField(default=0) 
  
  def __str__(self):
      return self.userRut

  def getUserExtended(userID):
      return commonUserModel.objects.get(id = userID)
      
