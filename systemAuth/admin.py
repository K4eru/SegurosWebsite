from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.commonUserModel)
admin.site.register(models.company)
admin.site.register(models.training)
admin.site.register(models.order)
admin.site.register(models.checklist)