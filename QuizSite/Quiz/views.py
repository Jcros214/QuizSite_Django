from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'Quiz/index.html')

def quiz(request):
    return render(request, 'Quiz/quiz.html')