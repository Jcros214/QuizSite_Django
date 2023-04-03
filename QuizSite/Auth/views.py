from django.shortcuts import render

from Records.models import Orginization

# Create your views here.
def register(request):

    context = {
        "churches": Orginization.objects.all()
    }

    return render(request, 'auth/register.html', context=context)