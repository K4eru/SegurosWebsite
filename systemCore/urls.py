from django.urls import path
from systemAuth.views import home
from .views import register, register_order

urlpatterns = [
    path('index', home, name ='home'),
    path('profile', register_order, name ='profile_details')
]