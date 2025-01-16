from django.contrib import admin
from .models import Enquiry, DispatchAgent, Hospital, Source, jdlead


admin.site.register(Enquiry)
admin.site.register(jdlead)


admin.site.register(DispatchAgent)
admin.site.register(Hospital)
admin.site.register(Source)



# Register your models here.

