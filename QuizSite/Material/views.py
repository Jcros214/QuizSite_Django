from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'Material/material.html')

def current_material(request):
    return index(request)