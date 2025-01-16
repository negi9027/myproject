from django.urls import path, include
from . import views


urlpatterns = [
    ######################## ENQUIRY ########################################

    path('addenquiry',views.add_enquiry),
    path('getenquiries',views.getenquiries), 
    path('editenquiry',views.edit_enquiry),
    path('dashboard',views.dashboard), 

    

]