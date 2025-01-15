from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from myproject import database

# Create your views here.





@csrf_exempt
def add_knowledge(request):
    if request.method == "POST":
        data = json.loads(request.body)
        table_name = 'knowledgebank'
        try:
            data['question']
            data['answer']
            data['profile']
            data['user_id']



        except:
            return JsonResponse({"success": False, "message": " 'user_id', 'profile', 'question', and 'answer' are mandatory to add any knowledge."})
        print(table_name)
        result = database.add_record(table_name, data)
        return JsonResponse(result)
    return JsonResponse({"success": False, "message": "Invalid request method"})

@csrf_exempt
def edit_knowledge(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            table_name = 'knowledgebank'  # table
            primary_key = data.get('knowledge_id')
            updated_fields = data.get("fields", {})
            if not primary_key or not updated_fields:
                return JsonResponse({"success": False, "message": "'name' Parameter and fields are required"})

            result = database.update_record(table_name, "name", primary_key, updated_fields)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

@csrf_exempt
def delete_knowledge(request):
    if request.method == "POST":
        data = json.loads(request.body)
        table_name = "knowledgebank"  # table
        primary_key = data.get("knowledge_id")
        primary_key_name = 'knowledge_id'
        result = database.delete_record(table_name, primary_key_name, primary_key)
        return JsonResponse(result)
    return JsonResponse({"success": False, "message": "Invalid request method"})


@csrf_exempt 
def getknowledges(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            data['profile']


        except:
            return JsonResponse({"success": False, "message": " 'profile' is mandatory to get any knowledge."})
        # Fetch all source records
        table_name = "knowledgebank"
        fields = {"profile":data.get('profile')}
        return database.filter_data(table_name,fields)

    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)