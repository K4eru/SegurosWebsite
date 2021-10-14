from django.db import models
from django.db.models.enums import TextChoices
from django.db.models.fields import TextField

#clienteTypes = ['Administrador', 'Cliente', 'Profesional' ]

class MainCliente(models.Model):
    userRut = TextField(30)
    userEmail = TextField(30)
  #  userType = TextChoices(clienteTypes)
    



