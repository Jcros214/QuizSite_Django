from django.contrib.admin.views.decorators import staff_member_required
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
            return {'object_list': League.objects.all()}
        case 1:
            return {
                'league': get_object_or_404(League, pk=args[0]),
                'object_list': Season.objects.filter(league_id=args[0]),
            }
        case 2:
            return {
                'league': get_object_or_404(League, pk=args[0]),
                'season': get_object_or_404(Season, pk=args[1]),
                'teams': get_object_or_404(Season, pk=args[1]).get_teams(),
                'object_list': Event.objects.filter(season_id=args[1]),
            }
        case 3:
            context = {
                'league': get_object_or_404(League, pk=args[0]),
                'season': get_object_or_404(Season, pk=args[1]),
            }

            if kwargs.get("team", False):
                context['object_list'] = [_.individual for _ in TeamMembership.objects.filter(team_id=args[2])]
                context['team'] = get_object_or_404(Team, pk=args[2])
            else:
                context['object_list'] = Quiz.objects.filter(event_id=args[2])
                context['event'] = get_object_or_404(Event, pk=args[2])
            return context

        case 4:
            return {
                'league': get_object_or_404(League, pk=args[0]),
                'season': get_object_or_404(Season, pk=args[1]),
                'event': get_object_or_404(Event, pk=args[2]),
                'quiz': get_object_or_404(Quiz, pk=args[3]),
                'results': get_object_or_404(Quiz, pk=args[3]).get_results(),
                'object_list': AskedQuestion.objects.filter(quiz_id=args[3]),
            }
        case 5:
            return {
                'league': get_object_or_404(League, pk=args[0]),
                'season': get_object_or_404(Season, pk=args[1]),
                'event': get_object_or_404(Event, pk=args[2]),
                'quiz': get_object_or_404(Quiz, pk=args[3]),
                'question': get_object_or_404(AskedQuestion, pk=args[4]),
            }


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
    return render(request, "Records/league_list.html", make_context())


# List of seasons
# @login_required
def league(request, league_id):
    return render(request, "Records/league.html", make_context(league_id))


# List of events
# @login_required
def season(request, league_id, season_id):
    # List of teams
    return render(request, "Records/season.html", make_context(league_id, season_id))


# List of quizes
# @login_required
def event(request, league_id, season_id, event_id):
    # get list of quizzes
    quizzes = Quiz.objects.filter(event_id=event_id)

    rooms = set()
    rounds = set()

    # find rounds
    for current_quiz in quizzes:
        rounds.add(int(current_quiz.round))
        rooms.add(current_quiz.room)

    quizzes_by_room = {}

    for room in sorted(rooms):
        quizzes_by_room[room] = []
        for current_quiz in sorted(quizzes.filter(room=room), key=lambda q: int(q.round)):
            quizzes_by_room[room].append(current_quiz)

    NEW_LINE = "\n"

    HTML = f'''
    <div style="overflow: scroll;">
<table>
    <tr>
        <th style="width: 40px"></th>
        {''.join(f"        <th class='round-number'> {_} </th> {NEW_LINE}" for _ in sorted([current_round for current_round in sorted(rounds)]))}
    </tr>
        
    '''

    for room in quizzes_by_room:
        HTML += f"""<tr><th>{room}</th>"""
        for current_quiz in quizzes_by_room[room]:
            HTML += f"""<td><a style="text-wrap: nowrap; padding: 6px;" href='/records/{league_id}/{season_id}/{event_id}/{current_quiz.id}'>{current_quiz}</a></td>"""
        HTML += "</tr>"
    HTML += "</table></div>"

    context = make_context(league_id, season_id, event_id)

    context['schedule'] = HTML
    context['current_round'] = context['event'].get_current_round()

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


@staff_member_required
def event_summary(request, event_id):
    event = Event.objects.get(id=event_id)
    quizzes = Quiz.objects.filter(event=event)

    # Initialize the pivot table
    pivot_table = {}

    # Iterate through quizzes
    for quiz in quizzes:
        # Get asked questions for each quiz
        asked_questions = AskedQuestion.objects.filter(quiz=quiz)

        # Iterate through asked questions
        for question in asked_questions:
            individual = question.individual

            if individual is None:
                continue

            if individual not in pivot_table:
                # Initialize the individual's record
                pivot_table[individual] = {
                    'total_points': 0,
                    'total_questions': 0,
                    'correct_questions': 0,
                    'accuracy': 0,
                }

            # Add the question's value to the total points
            pivot_table[individual]['total_points'] += question.value or 0

            # Count the total and correct questions
            pivot_table[individual]['total_questions'] += 1
            if question.ruling == 'correct':  # Assuming "Correct" indicates a correct answer
                pivot_table[individual]['correct_questions'] += 1

            # Calculate the accuracy
            pivot_table[individual]['accuracy'] = (
                    pivot_table[individual]['correct_questions'] / pivot_table[individual]['total_questions']
            )

    context = {
        'event': event,
        'pivot_table': pivot_table,
    }
    return render(request, 'admin/event_summary.html', context)
