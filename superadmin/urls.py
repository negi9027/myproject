from django.urls import path, include
from . import views


urlpatterns = [
    ######################## SUPER ADMIN AUTHENTICATION ########################################

    path('createadmin', views.index),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('check_login', views.check_login, name='check_login'),

    ######################## SOURCE ########################################

    path('editsource', views.edit_source, name='edit_record'),
    path('addsource', views.add_source, name='add_record'),
    path('deletesource', views.delete_source, name='delete_record'),
    path('getsources', views.getsources, name='getsources'),

    ######################## JUST DIAL ########################################

    path('justdialLeads',views.handle_leads),
    path('jdcrm',views.lead_list),


    ######################## HOSPITALS ########################################
    path('addhospital', views.add_hospital, name='add_hospital'),
    path('edithospital', views.edit_hospital, name='edit_hospital'),
    path('deletehospital', views.delete_hospital, name='delete_hospital'), 
    path('gethospitals', views.gethospitals, name='gethospitals'),

######################## MEDICINES ########################################
    path('addmedicine', views.add_medicine, name='add_medicine'),
    path('editmedicine', views.edit_medicine, name='edit_medicine'),
    path('deletemedicine', views.delete_medicine, name='delete_medicine'), 
    path('getmedicines', views.getmedicines, name='getmedicines'),



    ######################## USERS ########################################
    path('adduser', views.add_user, name='add_user'),
    path('edituser', views.edit_user, name='edit_user'),
    path('getusers', views.getusers, name='delete_hospital'), 
    path('deleteuser', views.delete_user, name='delete_user'),


    ######################  FILTER ##########################################

    path('filters',views.filters, name="filters"),
    path('specificrecord',views.specificrecord, name="specificrecord"),



    ####################   PROCESSES ############################################

    path('addprocess', views.add_process, name='add_process'),
    path('editprocess', views.edit_process, name='edit_process'),
    path('getprocesses', views.getprocesses, name='delete_hospital'), 
    path('deleteprocess', views.delete_process, name='delete_process'),


     ####################   DISEASE ############################################

    path('adddisease', views.add_disease, name='add_disease'),
    path('editdisease', views.edit_disease, name='edit_disease'),
    path('getdiseases', views.getdiseases, name='delete_hospital'), 
    path('deletedisease', views.delete_disease, name='delete_disease'),


  ####################   NOTIFICATION ############################################

    path('addnotification', views.add_notification, name='add_notification'),
    path('getnotifications', views.getnotifications, name='delete_hospital'), 



    ####################   KRA ############################################

    path('addkra', views.add_kra, name='add_kra'),
    path('editkra', views.edit_kra, name='edit_kra'),
    path('getkras', views.getkras, name='delete_hospital'), 
    path('deletekra', views.delete_kra, name='delete_disease'),


  ####################   TIME-TABLE ############################################

    path('addtimetable', views.add_timetable, name='add_timetable'),
    path('edittimetable', views.edit_timetable, name='edit_timetable'),
    path('gettimetables', views.gettimetables, name='delete_hospital'), 
    path('deletetimetable', views.delete_timetable, name='delete_disease'),
    path('appendtimetable',views.append_timetable_data),

  ####################   DISPOSITIONS ############################################

    path('adddisposition', views.add_disposition, name='add_disposition'),
    path('editdisposition', views.edit_disposition, name='edit_disposition'),
    path('getdispositions', views.getdispositions, name='delete_hospital'), 
    
]
