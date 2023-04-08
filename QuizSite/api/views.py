from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
def getRecords(request):
    return HttpResponse("Hello, world. You're at the api index.")