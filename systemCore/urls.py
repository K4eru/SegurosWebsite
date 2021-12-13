from django.urls import path
from systemAuth.views import home
from .views import  generatePDFGlobal,show_clientPayment, update_checklist, update_profile ,submit_Order , submit_training, show_training , show_order, update_order, submit_checklist,show_checklist,register_company,generatePDFClients

urlpatterns = [
    path('', home, name ='home'),
    path('profile', update_profile, name ='profile_details'),
    path('registerCompany', register_company, name ='registerCompany'),
    path('submit-order', submit_Order, name ='order'),
    path('submit-training', submit_training, name='submit-training'),
    path('show-training',show_training, name='show_training'),
    path('show-order',show_order, name='show_order'),
    path('edit-order/<int:order_pk>',update_order, name='edit_order'),
    path('edit-checklist/<int:checklist_pk>',update_checklist, name='edit_checklist'),
    path('submit-checklist',submit_checklist, name='submit_checklist'),
    path('show-checklist',show_checklist, name='show_checklist'),
    path('show-clientPayment',show_clientPayment, name='show_clientPayment'),
    path('generatePDFGlobal',generatePDFGlobal, name='generatePDF_global'),
    path('generatePDFCliente',generatePDFClients, name='generatePDF_client')
]