from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'quiz_games/index.html')


def match_verse_with_number(request):
    return render(request, 'quiz_games/match_verse_with_number.html')
