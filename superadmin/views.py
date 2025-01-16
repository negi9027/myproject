from django.shortcuts import render 
from django.shortcuts import HttpResponse
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from myproject import database
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.paginator import Paginator
from .models import Superadmin, jdlead
from django.db.models import Max
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist

from superadmin.models import kra, timetable



##################################################### SUPER ADMIN AUTHENTICATION#########################################
def index(request):
    superadmin = Superadmin.objects.create(username='admin', password=make_password("admin"))
    superadmin.save()
    return HttpResponse("HEY THERE")



@csrf_exempt
def login(request):
    if request.method == 'POST':
        # Get data from the POST request
        received_data = json.loads(request.body.decode('utf-8'))
        username = received_data.get('username')
        password = received_data.get('password')
        print(username,password)
        # Check if username and password are provided
        if not username or not password:
            return JsonResponse({"error": "Please provide both username and password"}, status=400)
        try:
            # Try to get the superadmin record
            superadmin = Superadmin.objects.get(username=username)

            # Check if the password matches
            if check_password(password, superadmin.password):
                # Store username in session on successful login
                request.session['username'] = superadmin.username
                return JsonResponse({"message": "Login successful"}, status=200)
            else:
                return JsonResponse({"error": "Invalid password"}, status=400)
        except Superadmin.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    else:
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)

@csrf_exempt
def logout(request):
    try:
        # Delete the session data
        del request.session['username']
        return JsonResponse({"message": "Logout successful"}, status=200)
    except KeyError:
        return JsonResponse({"error": "No active session"}, status=400)
    


@csrf_exempt
def check_login(request):
    # Check if the user is logged in (if the username exists in the session)
    if 'username' in request.session:
        return JsonResponse({"message": "User is logged in", "username": request.session['username']}, status=200)
    else:
        return JsonResponse({"error": "User is not logged in"}, status=400)
    


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




##########################################################SOURCE#############################################################

@csrf_exempt
def add_source(request):
    if request.method == "POST":
        data = json.loads(request.body)
        table_name = "source"
        record_data = data
        result = database.add_record(table_name, record_data)
        return JsonResponse(result)
    return JsonResponse({"success": False, "message": "Invalid request method"})



@csrf_exempt
def edit_source(request):
    if request.method == "POST":
        data = json.loads(request.body)
        table_name = "source"
        primary_key = data.get("name")
        updated_fields = data.get("fields", {})
        primary_key_name = 'name'
        result = database.update_record(table_name,primary_key_name, primary_key, updated_fields)
        return JsonResponse(result)
    return JsonResponse({"success": False, "message": "Invalid request method"})



@csrf_exempt
def delete_source(request):
    if request.method == "POST":
        data = json.loads(request.body)
        table_name = "source"
        primary_key = data.get("name")
        primary_key_name = 'name'
        result = database.delete_record(table_name, primary_key_name, primary_key)
        return JsonResponse(result)
    return JsonResponse({"success": False, "message": "Invalid request method"})



@csrf_exempt
def getsources(request):
    if request.method == "GET":
        # Fetch all source records
        return database.view_all_records('source')
        
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)
 




##################################################JUST-DIAL LEADS ######################################################


@csrf_exempt
def handle_leads(request):
        
    if request.method == "POST":

        received_data = json.loads(request.body)
# Construct the lead_data dictionary
        lead_data = {
            "leadid": received_data.get("leadid"),
            "leadtype": received_data.get("leadtype"),
            "prefix": received_data.get("prefix", ""),
            "name": received_data.get("name"),
            "mobile": received_data.get("mobile"),
            "phone": received_data.get("phone", ""),
            "email": received_data.get("email"),
            "date": received_data.get("date"),
            "category": received_data.get("category"),
            "area": received_data.get("area", ""),
            "city": received_data.get("city"),
            "brancharea": received_data.get("brancharea"),
            "dncmobile": received_data.get("dncmobile", 0),
            "dncphone": received_data.get("dncphone", 0),
            "company": received_data.get("company"),
            "pincode": received_data.get("pincode", 0),
            "time": received_data.get("time"),
            "branchpin": received_data.get("branchpin"),
            "parentid": received_data.get("parentid"),
        }

        print(lead_data)
        # Check for required fields
        required_fields = ["leadid", "leadtype", "name", "mobile"]
        missing_fields = [field for field in required_fields if not lead_data.get(field)]

        if missing_fields:
            return JsonResponse({
                "success": False,
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            })

        # Create new record in the database
        lead = jdlead.objects.create(**lead_data)


        return JsonResponse({"success": True, "message": "Lead added successfully"})
        
    
   
    return JsonResponse({"success": False, "message": "Invalid request method"})


def lead_list(request):
    # Get all the leads from the database
    leads = jdlead.objects.all()

    # Pass the data to the template
    print(leads)
    leads = jdlead.objects.all()  # Replace with your query
    paginator = Paginator(leads, 10)  # Show 10 leads per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(page_obj)

    return render(request, 'jdleads.html', {'page_obj': page_obj})





############################################### HOSPITAL #######################################################


@csrf_exempt
def add_hospital(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            table_name = "hospital"  # Model name
            result = database.add_record(table_name, data)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)


@csrf_exempt
def edit_hospital(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            table_name = "hospital"  # Model name
            primary_key = data.get("hospital_id")
            updated_fields = data.get("fields", {})
            if not primary_key or not updated_fields:
                return JsonResponse({"success": False, "message": "hospital_id and fields are required"})

            result = database.update_record(table_name, "hospital_id", primary_key, updated_fields)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)


@csrf_exempt
def delete_hospital(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            table_name = "hospital"  # Model name
            primary_key = data.get("hospital_id")
            if not primary_key:
                return JsonResponse({"success": False, "message": "hospital_id is required"})

            result = database.delete_record(table_name, "hospital_id", primary_key)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

@csrf_exempt
def gethospitals(request):
    if request.method == "GET":
        # Fetch all source records
        return database.view_all_records('hospital')
        
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)
 


############################################### MEDICINES ###################################################

@csrf_exempt
def add_medicine(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            table_name = "medicine"  # Model name
            result = database.add_record(table_name, data)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)


@csrf_exempt
def edit_medicine(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            table_name = "medicine"  # Model name
            primary_key = data.get("medicine_code")
            updated_fields = data.get("fields", {})
            if not primary_key or not updated_fields:
                return JsonResponse({"success": False, "message": "medicine_code and fields are required"})

            result = database.update_record(table_name, "medicine_code", primary_key, updated_fields)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)


@csrf_exempt
def delete_medicine(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            table_name = "medicine"  # Model name
            primary_key = data.get("medicine_code")
            if not primary_key:
               return JsonResponse({"success": False, "message": "medicine_code is required"})

            result = database.delete_record(table_name, "medicine_code", primary_key)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

@csrf_exempt
def getmedicines(request):
    if request.method == "GET":
        # Fetch all source records
        return database.view_all_records('medicine')
        
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)





########################################## USERS #############################################################
@csrf_exempt
def add_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            table_name = data['profile']
            name = data['name']

        except:
            return JsonResponse({"success": False, "message": "name and profile are required"})
        
        model_class = apps.get_model(app_label='superadmin', model_name=table_name)


        name = data['name']
        name_part = name[:3].upper()
        profile_part = data['profile'][:3].upper()

        # Get the current maximum counter value
        max_counter = model_class.objects.aggregate(Max('counter'))['counter__max'] or 0

        # Increment the counter
        new_counter = max_counter + 1
        print(new_counter)

        data['counter'] = new_counter

        # Format the user_id
        user_id = f"{profile_part}{name_part}{str(new_counter).zfill(3)}"
        data['user_id'] = user_id
        print(user_id)
        result = database.add_record(table_name, data)
        return JsonResponse(result)
    return JsonResponse({"success": False, "message": "Invalid request method"})

@csrf_exempt
def edit_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            table_name = data['profile']  # table
            primary_key = data.get("user_id")
            updated_fields = data.get("fields", {})
            if not primary_key or not updated_fields:
                return JsonResponse({"success": False, "message": "'user_id' Parameter and fields are required"})

            result = database.update_record(table_name, "user_id", primary_key, updated_fields)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

@csrf_exempt
def delete_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        table_name = data['profile']  # table
        primary_key = data.get("user_id")
        primary_key_name = 'user_id'
        result = database.delete_record(table_name, primary_key_name, primary_key)
        return JsonResponse(result)
    return JsonResponse({"success": False, "message": "Invalid request method"})


@csrf_exempt 
def getusers(request):
    if request.method == "POST":
        # Fetch all source records
        data = json.loads(request.body)
        table_name = data['profile']
        return database.view_all_records(table_name)
        
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

@csrf_exempt
def filters(request):
    if request.method == "POST":
        # Fetch all source records
        data = json.loads(request.body)
        table_name = data.get('filter')
        filters = data.get('fields')
        return database.filter_data(table_name, filters)
        
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

@csrf_exempt
def specificrecord(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            table_name = data['filter']
            pk_value = data['value']
            return database.specific_record(table_name,pk_value)
        except:
            return JsonResponse({"success": False, "message": "'filter' i.e. table name and 'value' i.e. primary key value is required." }, status=405)

    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)
    

########################################### PROCESSES ################################################################

@csrf_exempt
def add_process(request):
    if request.method == "POST":
        data = json.loads(request.body)
        table_name = 'process'
        try:
            data['name']
        except:
            return JsonResponse({"success": False, "message": "name is mandatory to add any process."})
        print(table_name)
        result = database.add_record(table_name, data)
        return JsonResponse(result)
    return JsonResponse({"success": False, "message": "Invalid request method"})

@csrf_exempt
def edit_process(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            table_name = 'process'  # table
            primary_key = data.get('name')
            updated_fields = data.get("fields", {})
            if not primary_key or not updated_fields:
                return JsonResponse({"success": False, "message": "'name' Parameter and fields are required"})

            result = database.update_record(table_name, "name", primary_key, updated_fields)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

@csrf_exempt
def delete_process(request):
    if request.method == "POST":
        data = json.loads(request.body)
        table_name = "process"  # table
        primary_key = data.get("name")
        primary_key_name = 'name'
        result = database.delete_record(table_name, primary_key_name, primary_key)
        return JsonResponse(result)
    return JsonResponse({"success": False, "message": "Invalid request method"})


@csrf_exempt 
def getprocesses(request):
    if request.method == "GET":
        # Fetch all source records
        table_name = "process"
        return database.view_all_records(table_name)

    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)




########################################### DISEASE ################################################################

@csrf_exempt
def add_disease(request):
    if request.method == "POST":
        data = json.loads(request.body)
        table_name = 'disease'
        try:
            data['name']
        except:
            return JsonResponse({"success": False, "message": "name is mandatory to add any disease."})
        print(table_name)
        result = database.add_record(table_name, data)
        return JsonResponse(result)
    return JsonResponse({"success": False, "message": "Invalid request method"})

@csrf_exempt
def edit_disease(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            table_name = 'disease'  # table
            primary_key = data.get('name')
            updated_fields = data.get("fields", {})
            if not primary_key or not updated_fields:
                return JsonResponse({"success": False, "message": "'name' Parameter and fields are required"})

            result = database.update_record(table_name, "name", primary_key, updated_fields)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

@csrf_exempt
def delete_disease(request):
    if request.method == "POST":
        data = json.loads(request.body)
        table_name = "disease"  # table
        primary_key = data.get("name")
        primary_key_name = 'name'
        result = database.delete_record(table_name, primary_key_name, primary_key)
        return JsonResponse(result)
    return JsonResponse({"success": False, "message": "Invalid request method"})


@csrf_exempt 
def getdiseases(request):
    if request.method == "GET":
        # Fetch all source records
        table_name = "disease"
        return database.view_all_records(table_name)

    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)



########################################### NOTIFICATIONS ################################################################

@csrf_exempt
def add_notification(request):
    if request.method == "POST":
        data = json.loads(request.body)
        table_name = 'notification'
        try:
            data['text']
            data['users']
        except:
            return JsonResponse({"success": False, "message": "text and users are mandatory fields to send any notification."})

        result = database.add_record(table_name, data)
        return JsonResponse(result)
    return JsonResponse({"success": False, "message": "Invalid request method"})


@csrf_exempt 
def getnotifications(request):
    if request.method == "GET":
        # Fetch all source records
        table_name = "notification"
        return database.view_all_records(table_name)

    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)


########################################### KRAs ################################################################

@csrf_exempt
def add_kra(request):
    if request.method == "POST":
        data = json.loads(request.body)
        table_name = 'kra'
        try:
            data['profile']
            data['kras']
        except:
            return JsonResponse({"success": False, "message": "name,kras,and profile are mandatory fields to add any kra."})
        print(table_name)
        result = database.add_record(table_name, data)
        return JsonResponse(result)
    return JsonResponse({"success": False, "message": "Invalid request method"})

@csrf_exempt
def edit_kra(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            table_name = 'kra'  # table
            primary_key = data.get('profile')
            updated_fields = data.get("fields", {})
            if not primary_key or not updated_fields:
                return JsonResponse({"success": False, "message": "'profile' Parameter and fields are required"})

            result = database.update_record(table_name, "profile", primary_key, updated_fields)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

@csrf_exempt
def delete_kra(request):
    if request.method == "POST":
        data = json.loads(request.body)
        table_name = "kra"  # table
        primary_key = data.get("profile")
        primary_key_name = 'profile'
        result = database.delete_record(table_name, primary_key_name, primary_key)
        return JsonResponse(result)
    return JsonResponse({"success": False, "message": "Invalid request method"})


@csrf_exempt 
def getkras(request):
    if request.method == "GET":
        table_name = "kra"
        return database.view_all_records(table_name)
    else:
        return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)



########################################### TIME-TABLE ################################################################

@csrf_exempt
def add_timetable(request):
    if request.method == "POST":
        data = json.loads(request.body)
        table_name = 'timetable'
        try:
            data['users']
            data['timetable']

        except:
            return JsonResponse({"success": False, "message": "users, and timetable  are mandatory fields to add any kra."})
        print(table_name)
        result = database.add_record(table_name, data)
        return JsonResponse(result)
    return JsonResponse({"success": False, "message": "Invalid request method"})

@csrf_exempt
def edit_timetable(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            table_name = 'timetable'  # table
            primary_key = data.get('id')
            updated_fields = data.get("fields", {})
            if not primary_key or not updated_fields:
                return JsonResponse({"success": False, "message": "'id' Parameter and fields are required"})

            result = database.update_record(table_name, "id", primary_key, updated_fields)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

@csrf_exempt
def delete_timetable(request):
    if request.method == "POST":
        data = json.loads(request.body)
        table_name = "timetable"  # table
        primary_key = data.get("id")
        primary_key_name = 'id'
        result = database.delete_record(table_name, primary_key_name, primary_key)
        return JsonResponse(result)
    return JsonResponse({"success": False, "message": "Invalid request method"})


@csrf_exempt 
def gettimetables(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            try:
                data['user_id']
            except:
                return JsonResponse({"success": False, "message": "user_id is mandatory field to get any timetable"})
            


            tt = timetable.objects.get(id=data['user_id'])
            
        
        # Serialize the object to a dictionary
            timetable_data = {
                "id": tt.id,
                "profile": tt.profile,
                "created_at": tt.created_at,
                "timetable": tt.timetable,
            }

        # Return the data as a JSON response
            return JsonResponse(timetable_data, safe=False)

        except ObjectDoesNotExist:
        # Return a 404 response if the object does not exist
            return JsonResponse({"error": "Timetable not found for this user_id"}, status=404)  

    else:
        return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)
    


@csrf_exempt
def append_timetable_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # Try to get the Timetable instance by id
            timetable_instance, created = timetable.objects.get_or_create(id=data.get('user_id'), defaults={'profile': data.get('profile')})

            # If the timetable exists, append the new data to the timetable field
            timetable_instance.timetable.update(data.get('timetable'))  # Use update to merge new data into the timetable field

            # Save the updated instance
            timetable_instance.save()

            return JsonResponse({"success":True, "message":"Timetable updated successfully."})

            # Return the updated instance or newly created instance

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    else:
        return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)
        
          # Return the error message if any exception occurs










########################################### DISPOSITIONS ################################################################

@csrf_exempt
def add_disposition(request):
    if request.method == "POST":
        data = json.loads(request.body)
        table_name = 'disposition'
        try:
            data['dispositions']
        except:
            return JsonResponse({"success": False, "message": "disposition  is mandatory field to add disposition."})
        result = database.add_record(table_name, data)
        return JsonResponse(result)
    return JsonResponse({"success": False, "message": "Invalid request method"})

@csrf_exempt
def edit_disposition(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            table_name = 'disposition'  # table
            primary_key = data.get('id')
            updated_fields = data.get("fields", {})
            if not primary_key or not updated_fields:
                return JsonResponse({"success": False, "message": "'id' Parameter and fields are required"})

            result = database.update_record(table_name, "id", primary_key, updated_fields)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)


@csrf_exempt 
def getdispositions(request):
    if request.method == "GET":
        table_name = "disposition"
        return database.view_all_records(table_name)
    else:
        return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)
