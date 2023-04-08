from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from Records.models import Orginization, Team, TeamMembership

# Create your views here.
def register(request):

    context = {
        "churches": Orginization.objects.all()
    }

    return render(request, 'auth/register.html', context=context)

@login_required
def profile(request): 
    context = {
        "teams": [_.team for _ in TeamMembership.objects.filter(individual_id=request.user.pk)],
    }

    return render(request, 'auth/profile.html', context=context)