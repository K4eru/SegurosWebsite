from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login', views.request_login, name='request_login'),
    path('register', views.register_user, name ='registerUser'),
    path('registerCompany', views.register_company, name ='registerCompany'),
    path('logout', LogoutView.as_view(), name='logout'),
]