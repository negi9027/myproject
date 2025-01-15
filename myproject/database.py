from django.apps import apps
from django.http import JsonResponse 
import json
from django.core.exceptions import ObjectDoesNotExist



def update_record(table_name, primary_key_name, primary_key, updated_fields):
    try:
        # Dynamically retrieve the model
        Model = apps.get_model(app_label="superadmin", model_name=table_name)
        
        # Use **{primary_key_name: primary_key} to dynamically pass the primary key field
        record = Model.objects.get(**{primary_key_name: primary_key})  # Dynamic field usage
        
        # Update fields if they exist in the model
        for field, value in updated_fields.items():
            if hasattr(record, field):
                setattr(record, field, value)
        
        # Save the updated record
        record.save()
        
        return {"success": True, "message": "Fields updated successfully"}
    
    except Model.DoesNotExist:
        return {"success": False, "message": "Record not found"}
    except LookupError:
        return {"success": False, "message": "Invalid table name"}
    except Exception as e:
        return {"success": False, "message": str(e)}







def add_record(table_name, record_data):
    try:
        Model = apps.get_model(app_label="superadmin", model_name=table_name)
        Model.objects.create(**record_data)
        return {"success": True, "message": "Record added successfully"}
    except LookupError as e:
        print(e)
        return {"success": False, "message": "Invalid table name"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def delete_record(table_name, primary_key_name, primary_key):
    try:
        Model = apps.get_model(app_label="superadmin", model_name=table_name)
        filter_kwargs = {primary_key_name: primary_key} if primary_key_name else primary_key
        record = Model.objects.get(**filter_kwargs)
        record.delete()
        return {"success": True, "message": "Record deleted successfully"}
    except Model.DoesNotExist:
        return {"success": False, "message": "Record not found"}
    except LookupError:
        return {"success": False, "message": "Invalid table name"}
    except Exception as e:
        return {"success": False, "message": str(e)}



def view_all_records(table_name):
    try:
        # Dynamically get the model for the given table name
        Model = apps.get_model(app_label="superadmin", model_name=table_name)
        
        # Retrieve all records from the model
        records = Model.objects.all()
        
        # Serialize the data (converting queryset to list of dictionaries)
        data = [record_to_dict(record) for record in records]
        
        return JsonResponse({"success": True, "data": data})
    
    except LookupError:
        return JsonResponse({"success": False, "message": "Invalid table name"})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})

def record_to_dict(record):
    """
    Helper function to convert a model record to a dictionary.
    """
    # Get all field names of the model
    fields = record._meta.get_fields()
    
    # Convert fields to a dictionary
    record_dict = {}
    for field in fields:
        if hasattr(record, field.name):
            record_dict[field.name] = getattr(record, field.name)
    
    return record_dict



def filter_data(table_name, filters):
   
    try:
        if not table_name:
            return JsonResponse({"success": False, "message": "Table name is required."}, status=400)
        
        # Dynamically retrieve the model
        Model = apps.get_model(app_label="superadmin", model_name=table_name)
        
        if not Model:
            return JsonResponse({"success": False, "message": "Invalid table name."}, status=400)
        
        # Apply filters to query the table
        queryset = Model.objects.filter(**filters).values()
        
        # Convert the queryset to a list of dictionaries
        results = list(queryset)
        
        return JsonResponse({"success": True, "data": results})
    
    except LookupError:
        return JsonResponse({"success": False, "message": "Table not found."}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)



def specific_record(table_name, pk_value):
    try:
        # Get the model dynamically based on the table name
        model = apps.get_model(app_label='superadmin', model_name=table_name)

        if not model:
            return JsonResponse({"error": "Invalid table name"}, status=400)

        # Fetch the record using the primary key
        record = model.objects.get(pk=pk_value)

        # Convert the record to a dictionary for JSON response
        record_data = {field.name: getattr(record, field.name) for field in model._meta.fields}

        return JsonResponse({"data": record_data}, status=200)

    except ObjectDoesNotExist:
        return JsonResponse({"error": "Record not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
