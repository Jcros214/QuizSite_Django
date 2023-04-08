from django.shortcuts import render, get_object_or_404
from .models import League, Season, Event, Quiz, AskedQuestion, TeamMembership, Individual, Team
from django.contrib.auth.decorators import login_required


# Create your views here.

    # context = {
    #     'league':     get_object_or_404(League, pk=league_id),
    #     'season':     get_object_or_404(Season, pk=season_id),
    #     'event':      get_object_or_404(Event, pk=event_id),
    #     'quiz':       get_object_or_404(Quiz, pk=quiz_id),
    #     'question':   get_list_or_404(AskedQuestion.objects.all()),
    # }


def make_context(*args, **kwargs):
    match len(args):
        case 0:
            return {'list': League.objects.all()}
        case 1:
            return {
                'league': get_object_or_404(League, pk=args[0]),
                'list': Season.objects.filter(league_id=args[0]),
            }
        case 2:
            return {
                'league': get_object_or_404(League, pk=args[0]),
                'season': get_object_or_404(Season, pk=args[1]),
                'teams': get_object_or_404(Season, pk=args[1]).getTeams(),
                'list': Event.objects.filter(season_id=args[1]),
            }
        case 3:
            context = {
                'league': get_object_or_404(League, pk=args[0]),
                'season': get_object_or_404(Season, pk=args[1]),
            }
            
            if kwargs.get("team", False):
                context['list'] = [_.individual for _ in TeamMembership.objects.filter(team_id=args[2])]
                context['team'] = get_object_or_404(Team, pk=args[2])
            else:
                context['list'] = Quiz.objects.filter(event_id=args[2])
                context['event'] = get_object_or_404(Event, pk=args[2])
            return context

        case 4:
            return {
                'league': get_object_or_404(League, pk=args[0]),
                'season': get_object_or_404(Season, pk=args[1]),
                'event': get_object_or_404(Event, pk=args[2]),
                'quiz': get_object_or_404(Quiz, pk=args[3]),
                'results': get_object_or_404(Quiz, pk=args[3]).getResults(),
                'list': AskedQuestion.objects.filter(quiz_id=args[3]),
            }
        case 5:
            return {
                'league': get_object_or_404(League, pk=args[0]),
                'season': get_object_or_404(Season, pk=args[1]),
                'event': get_object_or_404(Event, pk=args[2]),
                'quiz': get_object_or_404(Quiz, pk=args[3]),
                'question': get_object_or_404(AskedQuestion, pk=args[4]),
            }


# views.py
from django.views.generic import ListView
# from books.models import Publisher


class LeagueListView(ListView):
    model = League



# List of leagues
@login_required
def index(request):
    return LeagueListView.as_view()
    return render(request, "Records/index.html", make_context())

# List of seasons
@login_required
def league (request, league_id):
    return render(request, "Records/league.html", make_context(league_id))

# List of events
@login_required
def season (request, league_id, season_id):
    # List of teams
    return render(request, "Records/season.html", make_context(league_id, season_id))

# List of quizes
@login_required
def event (request, league_id, season_id, event_id):
    return render(request, "Records/event.html", make_context(league_id, season_id, event_id))

# List of questions
@login_required
def quiz (request, league_id, season_id, event_id, quiz_id):
    return render(request, "Records/quiz.html", make_context(league_id, season_id, event_id, quiz_id))

@login_required
def question (request, league_id, season_id, event_id, quiz_id, question_id):
    return render(request, "Records/question.html", make_context(league_id, season_id, event_id, quiz_id, question_id))

@login_required
def team (request, league_id, season_id, team_id):
    return render(request, "Records/team.html", make_context(league_id, season_id, team_id, team=True))

@login_required
def individual(request, individual_id):
    individual = get_object_or_404(Individual, pk=individual_id)
    teams = [_.team for _ in TeamMembership.objects.filter(individual_id=individual_id)]
    return render(request, "Records/individual.html", {'individual': individual, 'teams': teams})