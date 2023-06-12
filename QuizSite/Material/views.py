from django.shortcuts import render


# Create your views here.

# def index(request):
#     return render(request, 'Material/index.html', )
#

def render_material(request, name):
    return render(request, f'Material/{name}.html')


def current_material(request):
    return render_material(request, 'matthew_5_7')


def matthew(request):
    return render_material(request, 'matthew')
