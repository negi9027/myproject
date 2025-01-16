from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.utils.timezone import now


# your_app/views.py

from django.contrib.auth.decorators import login_required
from myproject import database
from superadmin.models import notification
from django.db.models import Q
from superadmin.models import process, disease, Source



@login_required
def addenquiry(request):
    print('working')
    return JsonResponse({"status":"working now."})


@csrf_exempt
def add_enquiry(request):
    if request.method == "POST":
        data = json.loads(request.body)
        table_name = "enquiry"
        record_data = data
        result = database.add_record(table_name, record_data)
        return JsonResponse(result)
    else:
        return JsonResponse({"success": False, "message": "Invalid request method"})

@csrf_exempt
def getenquiries(request):
    if request.method == "GET":
        # Fetch all source records
        return database.view_all_records('enquiry')
        
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)


@csrf_exempt
def edit_enquiry(request):
    if request.method == "POST":
        data = json.loads(request.body)
        table_name = "enquiry"
        primary_key = data.get("enquiry_id")
        updated_fields = data.get("fields", {})
        primary_key_name = 'enquiry_id'
        result = database.update_record(table_name,primary_key_name, primary_key, updated_fields)
        return JsonResponse(result)
    return JsonResponse({"success": False, "message": "Invalid request method"})



@csrf_exempt
def dashboard(request):
    if request.method == "POST":
        requestData = json.loads(request.body)
        userid = requestData.get('user_id')
        print(userid)
        data = []
# Fetch sources where dme contains userid
        sources = Source.objects.filter(dmes__contains=[str(userid)])
        print(sources)

        for source in sources:
            print(source)
            process_name = source.process_name  # Assuming process_name is a CharField in Source

            # Step 2: Fetch the related process
            try:
                proc = process.objects.get(name=process_name)

                # Step 3: Fetch the related disease
                disease_name = proc.disease  # Assuming disease is a CharField in process
                try:
                    dis = disease.objects.get(name=disease_name)

                    # Step 4: Construct the result data
                    data.append({
                        "name": source.name,
                        "process_name": proc.name,
                        "sub_disease": dis.sub_disease,
                        "disease":disease_name  # Assuming sub_disease is a list in disease
                    })
                except disease.DoesNotExist:
                    # Handle cases where no disease is found for the given process
                    continue
            except process.DoesNotExist:
                # Handle cases where no process is found for the process_name
                continue

        print(data)


        
        notifications = notification.objects.filter(unreadby__contains=[str(requestData.get('user_id'))])
        notifications_data = list(notifications.values()) 

        for noti in notifications:
            print(noti)
                
            unreadby_list = noti.unreadby or []
            print(unreadby_list)
            if userid in unreadby_list:
                unreadby_list.remove(userid)
                noti.unreadby = unreadby_list
                noti.save()

                
        return JsonResponse({"sources":data,"notifications":notifications_data})
