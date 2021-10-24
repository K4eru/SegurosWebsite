from django.db import models
from django.contrib.auth.models import User

CLIENT_TYPES = ((0, 'Administrador' ),
                (1, 'Cliente'),
                (2 ,'Profesional' ))

class commonUserModel(models.Model):
  
  user = models.OneToOneField(User, on_delete = models.CASCADE, related_name="extend")  
  userRut = models.CharField(max_length=20)
  userType = models.IntegerField(choices=CLIENT_TYPES, default=1)

  def __str__(self):
      return self.userRut

