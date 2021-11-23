from django.urls import path
from systemAuth.views import home
from .views import  update_profile , submit_Order , submit_training

urlpatterns = [
    path('', home, name ='home'),
    path('profile', update_profile, name ='profile_details'),
    path('submit-order', submit_Order, name ='order'),
    path('submit-training', submit_training, name='submit-training'),
    
]