from django.urls import path, include
from . import views


urlpatterns = [
    ######################## ENQUIRY ########################################

      path('addknowledge', views.add_knowledge, name='add_knowledge'),
    path('editknowledge', views.edit_knowledge, name='edit_knowledge'),
    path('getknowledges', views.getknowledges), 
    path('deleteknowledge', views.delete_knowledge),


]