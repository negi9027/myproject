from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from superadmin.models import Source
from django.utils.timezone import now


# your_app/views.py

from django.contrib.auth.decorators import login_required
from myproject import database
from superadmin.models import process,CallingAgent,Enquiry


@csrf_exempt
def dashboard(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            user_id = data['user_id']
        except:
            return JsonResponse({"status":False,"message": 'user_id is a mandatory field.'})
        ca = CallingAgent.objects.get(user_id=user_id)

        # Ensure the enquiry field is a list
        enquiry_ids = ca.enquiry if isinstance(ca.enquiry, list) else []

        # Fetch Enquiry records where the ID is in the enquiry list
        enquiries = Enquiry.objects.filter(enquiry_id__in=enquiry_ids)

        # Convert the queryset to a list of dictionaries
        data = list(enquiries.values("address","date","disease","dme_message","duplicate","enquiry_id","name","status","phone_number","sub_disease","working"))

        print(data)

        return JsonResponse({"status": True, "data": data})
    else:
        return JsonResponse({"status": False, "message": "Invalid request method"})


