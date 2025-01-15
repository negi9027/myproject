from django.shortcuts import render , redirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse
from django.http import JsonResponse
import json
from superadmin.models import jdlead
from django.core.paginator import Paginator
from django.db.models import Min, Max
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.apps import apps
from superadmin.models import Processhead , teamleader, CallingAgent,Enquiry , notification

# ----------------------------------------------------------------------------------------------------------------------
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
# from django.http import JsonResponse

# def send_notification(request):
#     user_id = request.GET.get("user_id")
#     message = request.GET.get("message")

#     if not user_id or not message:
#         return JsonResponse({"error": "Invalid parameters"}, status=400)

#     channel_layer = get_channel_layer()
#     group_name = f"notifications_{user_id}"

#     async_to_sync(channel_layer.group_send)(
#         group_name,
#         {
#             "type": "send_notification",
#             "message": message,
#         }
#     )
#     return JsonResponse({"status": "Message sent"})
# ----------------------------------------------------------------------------------------------------------------------







class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs): 
        print('working psot')
        user_id = request.data.get('user_id')
        password = request.data.get('password')
        profile = request.data.get('profile')  # Class name from the POST request

         
        try:
            # Dynamically get the model class
            model_class = apps.get_model(app_label='superadmin', model_name=profile)
        except LookupError:
            return Response({"error": f"Invalid profile type: {profile}"}, status=400)

        # Authenticate user using CustomAuthentication
        try:
            user = model_class.objects.filter(user_id=user_id).first()
            print(user_id,user.user_id,password, user.password)
            if not user or user.password != password:
                return Response({"error": "Invalid user_id or password"}, status=401)
        except:
            return Response({"error": "Invalid user_id"}, status=401)

    
 
        # Generate JWT token 

        refresh = RefreshToken()
        refresh['user_id'] = user.user_id 
         # Embed your custom user identifier
        if profile != 'superadmin':
            refresh['is_enabled'] = user.is_enabled  # Include additional user data as needed
 
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })
    



@csrf_exempt
def logout(request):
    if request.method == 'POST':
        try:
            # Parse the JSON request body
            received_data = json.loads(request.body.decode('utf-8'))
            refresh_token = received_data.get('refresh')

            # Ensure the refresh token is provided
            if not refresh_token:
                return JsonResponse({"error": "Refresh token is required"}, status=400)

            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            return JsonResponse({"message": "Logout successful"}, status=200)

        except Exception as e:
            print(e)
            return JsonResponse({"error": "Invalid token or token already blacklisted"}, status=400)
    else:
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)




def form(request):
    print('working this is the form')
    return render (request,'form.html')





def jdcrm(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username.upper() == 'JDCRM':
            if password == 'JDCRM#4321':
                request.session['login'] = True
            else:
                return render(request,'jdcrmlogin.html',{"message":"wrong password."})
        else:
            return render(request,'jdcrmlogin.html',{"message":"invalid username."})
    
    if request.session.get('login'):
            leads = jdlead.objects.all().order_by('-date', 'contacted')  # New leads first and uninterested leads second

    # Total number of leads
            total_leads = leads.count()

            # Calculate average enquiries per day
            date_range = leads.aggregate( 
                earliest_date=Min('date'), 
                latest_date=Max('date')
            )
            print(date_range['earliest_date'],date_range['latest_date'])
            if date_range['earliest_date'] and date_range['latest_date']:
                # Calculate the number of days between the earliest and latest date
                days = (date_range['latest_date'] - date_range['earliest_date']).days + 1
                print(days)
                avg_enquiries_per_day = total_leads / days if days > 0 else total_leads
            else:
                # Default values if no leads are present
                avg_enquiries_per_day = 0
                days = 0

            # Paginate the results
            paginator = Paginator(leads, 10)  # Show 10 leads per page
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            # Render the template with additional context
            return render(
                request, 
                'jdleads.html', 
                {
                    'page_obj': page_obj,
                    'total_enquiries': total_leads,
                    'average_enquiries_per_day': round(avg_enquiries_per_day, 2),
                }
            )


    else:
        return render(request,'jdcrmlogin.html',{"message":None})



def jdcrmlogout(request):
    try:
        del request.session['login']
    except:
        return redirect('/jdcrm')
    return redirect('/jdcrm')




@csrf_exempt
def saveLeads(request):
    receivedData = json.loads(str(request.body, encoding='utf-8'))
    print(receivedData)
    return HttpResponse("done")
    

@csrf_exempt
def update_lead_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lead_id = data.get("lead_id")
            contacted = data.get("contacted")
            interested = data.get("interested")

            print(data)

            # Fetch the lead from the database
            lead = jdlead.objects.get(leadid=lead_id)
 
            # Update the fields based on the received data
            lead.contacted = contacted
            lead.contacted_on = data.get('contacted_on')
            lead.interested = interested if contacted else False  # If not contacted, don't allow interested
            lead.save()

            return JsonResponse({"success": True, "message": "Lead status updated successfully"})

        except jdlead.DoesNotExist:
            return JsonResponse({"success": False, "message": "Lead not found"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Invalid request method"})


def changedatabase(request):
    try:
        # Update records where process_name is NULL or empty string
        teamleader.objects.filter(process_name__isnull=True).update(process_name=[])
        teamleader.objects.filter(process_name='').update(process_name=[])

        CallingAgent.objects.filter(process_name__isnull=True).update(process_name=[])
        CallingAgent.objects.filter(process_name='').update(process_name=[])

        Processhead.objects.filter(process_name__isnull=True).update(process_name=[])
        Processhead.objects.filter(process_name='').update(process_name=[])


        return JsonResponse({"success": True, "message": "Process name updated successfully for null or empty values."})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})
    


def checkwebsockets(request,a):
    return render(request,'websocks.html')




@csrf_exempt
def enquiry(request):
    if request.method == "POST":
        try:
            # Parse the request body
            data = json.loads(request.body)
            profile = data.get("profile")  # Table name from the request body
            user_id = data.get("user_id")  # User ID from the request body
            
            if not profile or not user_id:
                return JsonResponse({"success": False, "message": "Both profile and user_id are required."}, status=400)

            # Dynamically retrieve the model
            Model = apps.get_model(app_label="superadmin", model_name=profile)

            # Fetch the row for the given user_id
            process_head = Model.objects.filter(pk=user_id).values("enquiry").first()
            
            if not process_head or not process_head.get("enquiry"):
                return JsonResponse({"success": False, "message": "No enquiries found for the given user_id."}, status=404)

            # Extract enquiry IDs from the retrieved row
            enquiry_ids = process_head.get("enquiry", [])
            
            # Fetch all the enquiries with the given IDs
            enquiries = Enquiry.objects.filter(pk__in=enquiry_ids).values()
            
            return JsonResponse({"success": True, "enquiries": list(enquiries)})

        except LookupError as e:
            print(e)
            return JsonResponse({"success": False, "message": "Invalid table name."}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    else:
        return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)



@csrf_exempt
def notifications(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            data['user_id']
        except:
            return JsonResponse({"success": False, "message": "'user_id' is required."})
        
        
        notifications = notification.objects.filter(users__contains=[str(data.get('user_id'))])
        notifications_data = list(notifications.values()) 
        return JsonResponse({"success": True, "notifications": notifications_data})
    else:
        return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)


