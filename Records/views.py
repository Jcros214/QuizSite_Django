from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

from .models import *
from django.contrib.auth.decorators import login_required
from server_timing.middleware import TimedService, timed, timed_wrapper


# Create your views here.

# context = {
#     'league':     get_object_or_404(League, pk=league_id),
#     'season':     get_object_or_404(Season, pk=season_id),
#     'event':      get_object_or_404(Event, pk=event_id),
#     'quiz':       get_object_or_404(Quiz, pk=quiz_id),
#     'question':   get_list_or_404(AskedQuestion.objects.all()),
# }


# def make_context(*args, **kwargs):
#     match len(args):
#         case 0:
#             return {'object_list': League.objects.all().order_by('name')}
#         case 1:
#             return {
#                 'league': get_object_or_404(League, pk=args[0]),
#                 'object_list': Season.objects.filter(league_id=args[0]).order_by('start_date'),
#             }
#         case 2:
#             return {
#                 'league': get_object_or_404(League, pk=args[0]),
#                 'season': get_object_or_404(Season, pk=args[1]),
#                 'teams': get_object_or_404(Season, pk=args[1]).get_teams().order_by('short_name'),
#                 'object_list': Event.objects.filter(season_id=args[1]).order_by('date'),
#             }
#         case 3:
#             context = {
#                 'league': get_object_or_404(League, pk=args[0]),
#                 'season': get_object_or_404(Season, pk=args[1]),
#             }
#
#             if kwargs.get("team", False):
#                 context['team'] = get_object_or_404(Team, pk=args[2])
#                 context['object_list'] = context['team'].individuals.all().order_by('name')
#             else:
#                 context['object_list'] = Quiz.objects.filter(event_id=args[2]).order_by('round', 'room')
#                 context['event'] = get_object_or_404(Event, pk=args[2])
#             return context
#
#         case 4:
#             quiz = get_object_or_404(Quiz, pk=args[3])
#             return {
#                 'league': get_object_or_404(League, pk=args[0]),
#                 'season': get_object_or_404(Season, pk=args[1]),
#                 'event': get_object_or_404(Event, pk=args[2]),
#                 'quiz': quiz,
#                 'results': quiz.get_results(),
#                 'object_list': AskedQuestion.objects.filter(quiz=quiz),
#             }
#         case 5:
#             return {
#                 'league': get_object_or_404(League, pk=args[0]),
#                 'season': get_object_or_404(Season, pk=args[1]),
#                 'event': get_object_or_404(Event, pk=args[2]),
#                 'quiz': get_object_or_404(Quiz, pk=args[3]),
#                 'question': get_object_or_404(AskedQuestion, pk=args[4]),
#             }


# # views.py
# from django.views.generic import ListView
# from django.contrib.auth.mixins import LoginRequiredMixin

# # from books.models import Publisher


# class LeagueListView(LoginRequiredMixin, ListView):
#     model = League

#     context = make_context()

#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     from django.utils import timezone
#     #     context['now'] = timezone.now()
#     #     return context


#     # template_name = ''


# List of leagues
# @login_required
def index(request):
    return render(request, "Records/league_list.html", {'object_list': League.objects.all()})


# List of seasons
# @login_required
def league(request, league_id):
    return render(request, "Records/league.html", make_context(league_id))


# List of events
# @login_required
def season(request, season_id):
    # List of teams
    return render(request, "Records/season.html", make_context(league_id, season_id))


# List of quizes
# @login_required
# @timed_wrapper('event', 'Event View')
def event(request, event_id):
    #     # get list of quizzes
    #     quizzes = Quiz.objects.filter(event_id=event_id)
    #
    #     rooms = set()
    #     rounds = set()
    #
    #     # find rounds
    #     for current_quiz in quizzes:
    #         rounds.add(int(current_quiz.round))
    #         rooms.add(current_quiz.room)
    #
    #     quizzes_by_room = {}
    #
    #     for room in sorted(rooms, key=lambda r: str(r.name)):
    #         quizzes_by_room[room] = []
    #         for current_quiz in sorted(quizzes.filter(room=room), key=lambda q: int(q.round)):
    #             quizzes_by_room[room].append(current_quiz)
    #
    #     NEW_LINE = "\n"
    #
    #     HTML = f'''
    #     <div style="overflow: scroll;">
    # <table>
    #     <tr>
    #         <th style="width: 40px"></th>
    #         {''.join(f"        <th class='round-number'> {_} </th> {NEW_LINE}" for _ in sorted([current_round for current_round in sorted(rounds)]))}
    #     </tr>
    #
    #     '''
    #
    #     for room in quizzes_by_room:
    #         HTML += f"""<tr><th>{room}</th>"""
    #         for current_quiz in quizzes_by_room[room]:
    #             HTML += f"""<td><a style="text-wrap: nowrap; padding: 6px;" href='/records/{league_id}/{season_id}/{event_id}/{current_quiz.id}'>{" v ".join([str(quiz_team) for quiz_team in current_quiz.get_teams()])}</a></td>"""
    #         HTML += "</tr>"
    #     HTML += "</table></div>"

    context = make_context(league_id, season_id, event_id)
    # context['schedule'] = HTML

    return render(request, "Records/event.html", context)


# List of questions
# @login_required
def quiz(request, league_id, season_id, event_id, quiz_id):
    return render(request, "Records/quiz.html", make_context(league_id, season_id, event_id, quiz_id))


# @login_required
def question(request, league_id, season_id, event_id, quiz_id, question_id):
    return render(request, "Records/question.html", make_context(league_id, season_id, event_id, quiz_id, question_id))


# @login_required
def team(request, league_id, season_id, team_id):
    return render(request, "Records/team.html", make_context(league_id, season_id, team_id, team=True))


# @login_required
def individual(request, individual_id):
    individual = get_object_or_404(Individual, pk=individual_id)
    teams = [_.team for _ in TeamMembership.objects.filter(individual_id=individual_id)]
    return render(request, "Records/individual.html", {'individual': individual, 'teams': teams})


class LeagueDetailView(DetailView):
    model = League
    template_name = 'Records/league.html'


class SeasonDetailView(DetailView):
    model = Season
    template_name = 'Records/season.html'


class EventDetailView(DetailView):
    model = Event
    template_name = 'Records/event.html'


class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'Records/quiz.html'


class TeamDetailView(DetailView):
    model = Team
    template_name = 'Records/team.html'


class IndividualDetailView(DetailView):
    model = Individual
    template_name = 'Records/individual.html'


class QuestionDetailView(DetailView):
    model = AskedQuestion
    template_name = 'Records/question.html'
