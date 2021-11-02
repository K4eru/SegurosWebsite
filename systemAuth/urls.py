from django.urls import path
from . import views

urlpatterns = [
    path('login', views.request_login, name='request_login'),
    path('register', views.register_user, name ='request_register'),
]