from django.shortcuts import render
from .round_robin_scheduler import RoundRobinScheduler, Team, tabulate_rounds, find_fairness

# Create your views here.

def index(request):
    return render(request, 'Manager/index.html')

# def round_robbin(request):
#     if request.method == 'GET':
#         return render(request, 'manager/round_robbin.html')
#     elif request.method == 'POST':
#         team_names = request.POST.get('teamNames')
#         rounds = int(request.POST.get('rounds'))
#         rooms = int(request.POST.get('rooms'))
        
#         # Do something with the variables (e.g., generate matchups, calculate fairness metrics)

        


        
#         # Render the response with the variables
#         return render(request, 'manager/round_robbin.html', {
#             'team_names': team_names,
#             'rounds': rounds,
#             'rooms': rooms,
#         })
#     else:
#         raise Exception('Invalid request method')
    
def generate_matchups(request):
    if request.method == 'POST':
        team_names = request.POST.get('team_names').split(',')
        rounds = int(request.POST.get('rounds'))
        rooms = int(request.POST.get('rooms'))

        scheduler = RoundRobinScheduler(matches_per_round=rooms)
        scheduler.teams = [Team(name) for name in team_names]
        scheduler.create_matches()
        schedule = scheduler.rounds

        dict_schedule = tabulate_rounds(schedule, team_names[:rooms])

        fairness_metrics = find_fairness(scheduler.teams, dict_schedule)

        return render(request, 'Manager/round_robin_result.html', {'schedule': dict_schedule, 'fairness_metrics': fairness_metrics})

    return render(request, 'Manager/round_robin.html')
