from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse
from .models import Season, Event, Quiz, AskedQuestion

# Create your views here.

# List of seasons
def index(request):
    context = {
        'seasons': get_list_or_404(Season.objects.all()),
    }
    return render(request, "Records/index.html", context)

# List of events
def season(request, season_id):
    context = {
        'season': get_object_or_404(Season, pk=season_id),
        'events': get_list_or_404(Event.objects.all())
        }
    return render(request, "Records/season.html", context)
    # return HttpResponse(Season.objects.get(pk=season_id))

# List of quizes
def event(request, season_id, event_id):
    quizes = get_list_or_404(Quiz.objects.all())
    context = {
        'season': get_object_or_404(Season, pk=season_id),
        'event': get_object_or_404(Event, pk=event_id),
        'quizes': get_list_or_404(Quiz.objects.all()),
    }
    return render(request, "Records/event.html", context)
    # return HttpResponse(Event.objects.get(pk=event_id))

# List of questions
def quiz(request, season_id, event_id, quiz_id):
    questions = get_list_or_404(AskedQuestion.objects.all())
    context = {
        'season': get_object_or_404(Season, pk=season_id),
        'event': get_object_or_404(Event, pk=event_id),
        'quiz': get_object_or_404(Quiz, pk=quiz_id),
        'questions': get_list_or_404(AskedQuestion.objects.all()),
    }
    return render(request, "Records/quiz.html", context)
    # return HttpResponse(Quiz.objects.get(pk=quiz_id))

def question(request, season_id, event_id, quiz_id, question_id):
    question = get_object_or_404(AskedQuestion, pk=question_id)
    context = {
        'season': get_object_or_404(Season, pk=season_id),
        'event': get_object_or_404(Event, pk=event_id),
        'quiz': get_object_or_404(Quiz, pk=quiz_id),
        'question': get_object_or_404(AskedQuestion, pk=question_id),
    }
    return render(request, "Records/question.html", context)
    # return HttpResponse(AskedQuestion.objects.get(pk=question_id))