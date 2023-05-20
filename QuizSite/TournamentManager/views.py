from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'manager/index.html')

def round_robbin(request):
    if request.method == 'GET':
        return render(request, 'manager/round_robbin.html')
    elif request.method == 'POST':
        team_names = request.POST.get('teamNames')
        rounds = int(request.POST.get('rounds'))
        rooms = int(request.POST.get('rooms'))
        
        # Do something with the variables (e.g., generate matchups, calculate fairness metrics)

        


        
        # Render the response with the variables
        return render(request, 'manager/round_robbin.html', {
            'team_names': team_names,
            'rounds': rounds,
            'rooms': rooms,
        })
