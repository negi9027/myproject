from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from superadmin.models import Processhead, CallingAgent, teamleader, Enquiry


@csrf_exempt
def     dashboard(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get('user_id')
        team_leaders = teamleader.objects.filter(process_head=user_id).values('user_id', 'name')
        print('team leaders', list(team_leaders))
        # Prepare the result dictionary
        result = {}

        for team_leader in team_leaders:
            team_leader_id = team_leader['user_id']
            team_leader_name = team_leader['name']
            
            # Fetch all calling agents where team_leader = team_leader_id
            calling_agents = CallingAgent.objects.filter(team_leader=team_leader_id).values('user_id', 'name')
            
            # Add to the result dictionary
            result[team_leader_id] = {
                "team_leader_name": team_leader_name,
                "calling_agents": list(calling_agents)  # Convert QuerySet to list for serialization
            }
        
        print(result)
        return JsonResponse(result)
    else:
        return JsonResponse({"status":False,"message":"Invalid Request Method."})
    
