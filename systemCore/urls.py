from django.urls import path
from systemAuth.views import home
from .views import  update_profile , submit_Order , submit_training, show_training , show_order, update_order

urlpatterns = [
    path('', home, name ='home'),
    path('profile', update_profile, name ='profile_details'),
    path('submit-order', submit_Order, name ='order'),
    path('submit-training', submit_training, name='submit-training'),
    path('show-training',show_training, name='show_training'),
    path('show-order',show_order, name='show_order'),
    path('edit-order/<int:order_pk>',update_order, name='edit_order')
]