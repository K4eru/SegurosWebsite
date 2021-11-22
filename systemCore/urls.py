from django.urls import path
from systemAuth.views import home
from .views import  register_order , submit_Order

urlpatterns = [
    path('', home, name ='home'),
    path('profile', register_order, name ='profile_details'),
    path('submit-order', submit_Order, name ='order')

]