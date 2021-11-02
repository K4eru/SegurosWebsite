from django.urls import path
from systemAuth.views import home
from . import views

urlpatterns = [
    path('index', home, name ='home'),
    path('profile', views.profile, name ='profile_details')
]