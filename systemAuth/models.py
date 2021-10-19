from django.db import models
from django.contrib.auth.models import User

#clienteTypes = ['Administrador', 'Cliente', 'Profesional' ]

class commonUserModel(models.Model):
  
  user = models.OneToOneField(User, on_delete = models.CASCADE, related_name="extend")  
  userRut = models.TextField()
  userType = models.TextField()

  def __str__(self):
      return self.userRut

