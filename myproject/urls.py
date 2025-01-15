# myproject/urls.py
from django.contrib import admin
from django.urls import path , include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    # path('send-notification/', views.send_notification, name='send_notification'),

    path('admin/', admin.site.urls),
    path('api/superadmin/', include('superadmin.urls')), 
    path('api/dme/', include('dme.urls')),
    path('api/processhead/',include('processhead.urls')),
    path('api/callingagent/',include('callingagent.urls')), 
    path('api/knowledgebank/',include('knowledgebank.urls')),
    path('api/token', views.LoginAPIView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout', views.logout, name='token_logout'),    
    path('api/token/verify', TokenVerifyView.as_view(), name='token_verify'),    
    path('api/enquiry',views.enquiry),
    path('api/notifications',views.notifications),
    path('form/',views.form),
    path('jdcrm',views.jdcrm),
    path('jdcrm/logout',views.jdcrmlogout),
    path('saveLeads/',views.saveLeads),
    path('updatejdleads/',views.update_lead_status),
    path('changedatabase/',views.changedatabase),
path('checkwebsockets/<str:a>/', views.checkwebsockets),
]
