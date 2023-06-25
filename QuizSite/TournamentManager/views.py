from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render

from .round_robin_scheduler import RoundRobinScheduler, Team, tabulate_rounds, find_fairness
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

try:
    from Records.models import *
except ImportError:
    from ..Records.models import *


# Create your views here.

def index(request):
    return render(request, 'Manager/index.html')


def generate_matchups(request):
    if request.method == 'POST':
        team_names = request.POST.get('team_names').split(',')
        # rounds = int(request.POST.get('rounds'))
        rooms = int(request.POST.get('rooms'))

        scheduler = RoundRobinScheduler(matches_per_round=rooms)
        scheduler.teams = [Team(name) for name in team_names]
        scheduler.create_matches()
        schedule = scheduler.rounds

        dict_schedule = tabulate_rounds(schedule, team_names[:rooms])

        fairness_metrics = find_fairness(scheduler.teams, dict_schedule)

        return render(request, 'Manager/round_robin_result.html',
                      {'schedule': dict_schedule, 'fairness_metrics': fairness_metrics})

    return render(request, 'Manager/round_robin.html')


@login_required
def populate_round_robbin_event(request):
    if request.method != 'POST':
        return render(request, 'Manager/round_robin_event_maker.html')

    season = request.POST.get("season")
    # teams = request.POST.get("teams")
    # event = request.POST.get("event")
    # TODO: TMP; RM
    season = Season.objects.first()
    organization = Organization.objects.first()
    event = Event.objects.get(pk=4)

    # def get_team_by_name(team_name_str: str):
    #     try:
    #         return Team.objects.get(name=team_name_str)
    #     except (IntegrityError, Team.DoesNotExist):
    #         return Team.objects.create(name=team_name_str, organization=organization, season=season)
    #
    # def get_individual_by_name(name: str):
    #     try:
    #         return Individual.objects.get(name=name)
    #     except (IntegrityError, Individual.DoesNotExist):
    #         return Individual.objects.create(name=name, user=User.objects.create_user(name, password="password"))
    #
    # def get_team_membership(team_name_str: Team, individual: Individual):
    #     try:
    #         return TeamMembership.objects.get(team=team_name_str, individual=individual)
    #     except (IntegrityError, TeamMembership.DoesNotExist):
    #         return TeamMembership.objects.create(team=team_name_str, individual=individual)
    #
    # for team_name, team in zip(teams.keys(), teams.values()):
    #     new_team = get_team_by_name(team_name.strip())
    #     new_individuals = [
    #         get_individual_by_name(individual.strip()) for
    #         individual in team]
    #     [get_team_membership(new_team, individual) for individual in
    #      new_individuals]

    LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    teams = []

    for bracket in ["R", "B"]:
        for letter in LETTERS[:18]:
            teams.append(Team(short_name=bracket + letter, name='', organization=organization, season=season))

    Team.objects.bulk_create(teams)

    rooms = [
        [],  # Started counting from 1...
        ['A', "Nathan Crosby", "Abigail Crosby"],
        ['B', "Jim Cutler", "Jacqueline Cutler"],
        ['C', "Daniel Jones", "Debbie Eastland"],
        ['D', "Daniel Crosby", "Victoria Eastland"],
        ['E', "Heather Crosby", "Lydia Crosby"],
        ['F', "Michael Jones", "Danielle Crosby"],
        ['G', "Adam Eastland", "Emma Eastland"]
    ]

    matches = [
        {
            'room': rooms[1],
            'round': 1,
            'teams': ["RB", "RJ", "RR"]
        },
        {
            'room': rooms[1],
            'round': 2,
            'teams': ["BH", "BP", "BF"]
        },
        {
            'room': rooms[1],
            'round': 3,
            'teams': ["RH", "RP", "RC"]
        },
        {
            'room': rooms[1],
            'round': 4,
            'teams': ["BE", "BK", "BQ"]
        },
        {
            'room': rooms[1],
            'round': 5,
            'teams': ["RM", "RE", "RI"]
        },
        {
            'room': rooms[1],
            'round': 6,
            'teams': ["BA", "BJ", "BP"]
        },
        {
            'room': rooms[1],
            'round': 7,
            'teams': ["RN", "RC", "RJ"]
        },
        {
            'room': rooms[1],
            'round': 8,
            'teams': ["RB", "RD", "RF"]
        },
        {
            'room': rooms[1],
            'round': 9,
            'teams': ["RA", "RG", "RM"]
        },
        {
            'room': rooms[1],
            'round': 10,
            'teams': ["BG", "BO", "BB"]
        },
        {
            'room': rooms[1],
            'round': 11,
            'teams': ["RD", "RG", "RM"]
        },
        {
            'room': rooms[1],
            'round': 12,
            'teams': ["RN", "RP", "RR"]
        },

        {
            'room': rooms[2],
            'round': 1,
            'teams': ["RC", "RK", "RM"]
        },
        {
            'room': rooms[2],
            'round': 2,
            'teams': ["RL", "RH", "RJ"]
        },
        {
            'room': rooms[2],
            'round': 3,
            'teams': ["RI", "RQ", "RD"]
        },
        {
            'room': rooms[2],
            'round': 4,
            'teams': ["BF", "BL", "BR"]
        },
        {
            'room': rooms[2],
            'round': 5,
            'teams': ["RN", "RF", "RJ"]
        },
        {
            'room': rooms[2],
            'round': 6,
            'teams': ["BB", "BK", "BQ"]
        },
        {
            'room': rooms[2],
            'round': 7,
            'teams': ["RO", "RD", "RK"]
        },
        {
            'room': rooms[2],
            'round': 8,
            'teams': ["BR", "BA", "BH"]
        },
        {
            'room': rooms[2],
            'round': 9,
            'teams': ["RB", "RH", "RN"]
        },
        {
            'room': rooms[2],
            'round': 10,
            'teams': ["BH", "BP", "BC"]
        },
        {
            'room': rooms[2],
            'round': 11,
            'teams': ["RE", "RH", "RN"]
        },
        {
            'room': rooms[2],
            'round': 12,
            'teams': ["BO", "BA", "BK"]
        },

        {
            'room': rooms[3],
            'round': 1,
            'teams': ["RD", "RL", "RN"]
        },
        {
            'room': rooms[3],
            'round': 2,
            'teams': ["BI", "BQ", "BA"]
        },
        {
            'room': rooms[3],
            'round': 3,
            'teams': ["RJ", "RR", "RE"]
        },
        {
            'room': rooms[3],
            'round': 4,
            'teams': ["RA", "RC", "RE"]
        },
        {
            'room': rooms[3],
            'round': 5,
            'teams': ["BN", "BP", "BR"]
        },
        {
            'room': rooms[3],
            'round': 6,
            'teams': ["BC", "BL", "BR"]
        },
        {
            'room': rooms[3],
            'round': 7,
            'teams': ["RP", "RE", "RL"]
        },
        {
            'room': rooms[3],
            'round': 8,
            'teams': ["BM", "BB", "BI"]
        },
        {
            'room': rooms[3],
            'round': 9,
            'teams': ["RC", "RI", "RO"]
        },
        {
            'room': rooms[3],
            'round': 10,
            'teams': ["BI", "BQ", "BD"]
        },
        {
            'room': rooms[3],
            'round': 11,
            'teams': ["RF", "RI", "RO"]
        },
        {
            'room': rooms[3],
            'round': 12,
            'teams': ["BP", "BB", "BL"]
        },

        {
            'room': rooms[4],
            'round': 1,
            'teams': ["RE", "RG", "RO"]
        },
        {
            'room': rooms[4],
            'round': 2,
            'teams': ["BJ", "BR", "BB"]
        },
        {
            'room': rooms[4],
            'round': 3,
            'teams': ["RK", "RM", "RF"]
        },
        {
            'room': rooms[4],
            'round': 4,
            'teams': ["BA", "BG", "BM"]
        },
        {
            'room': rooms[4],
            'round': 5,
            'teams': ["RO", "RA", "RK"]
        },
        {
            'room': rooms[4],
            'round': 6,
            'teams': ["BD", "BG", "BM"]
        },
        {
            'room': rooms[4],
            'round': 7,
            'teams': ["RQ", "RF", "RG"]
        },
        {
            'room': rooms[4],
            'round': 8,
            'teams': ["BN", "BC", "BJ"]
        },
        {
            'room': rooms[4],
            'round': 9,
            'teams': ["RD", "RJ", "RP"]
        },
        {
            'room': rooms[4],
            'round': 10,
            'teams': ["BJ", "BR", "BE"]
        },
        {
            'room': rooms[4],
            'round': 11,
            'teams': ["BG", "BI", "BK"]
        },
        {
            'room': rooms[4],
            'round': 12,
            'teams': ["BQ", "BC", "BG"]
        },

        {
            'room': rooms[5],
            'round': 1,
            'teams': ["RF", "RH", "RP"]
        },
        {
            'room': rooms[5],
            'round': 2,
            'teams': ["BK", "BM", "BC"]
        },
        {
            'room': rooms[5],
            'round': 3,
            'teams': ["BO", "BQ", "BM"]
        },
        {
            'room': rooms[5],
            'round': 4,
            'teams': ["BB", "BH", "BN"]
        },
        {
            'room': rooms[5],
            'round': 5,
            'teams': ["RP", "RB", "RL"]
        },
        {
            'room': rooms[5],
            'round': 6,
            'teams': ["BE", "BH", "BN"]
        },
        {
            'room': rooms[5],
            'round': 7,
            'teams': ["BB", "BD", "BF"]
        },
        {
            'room': rooms[5],
            'round': 8,
            'teams': ["BO", "BD", "BK"]
        },
        {
            'room': rooms[5],
            'round': 9,
            'teams': ["RE", "RK", "RQ"]
        },
        {
            'room': rooms[5],
            'round': 10,
            'teams': ["BK", "BM", "BF"]
        },
        {
            'room': rooms[5],
            'round': 11,
            'teams': ["RA", "RJ", "RP"]
        },
        {
            'room': rooms[5],
            'round': 12,
            'teams': ["BR", "BD", "BH"]
        },

        {
            'room': rooms[6],
            'round': 1,
            'teams': ["BL", "BH", "BJ"]
        },
        {
            'room': rooms[6],
            'round': 2,
            'teams': ["BL", "BN", "BD"]
        },
        {
            'room': rooms[6],
            'round': 3,
            'teams': ["RL", "RN", "RA"]
        },
        {
            'room': rooms[6],
            'round': 4,
            'teams': ["BC", "BI", "BO"]
        },
        {
            'room': rooms[6],
            'round': 5,
            'teams': ["RQ", "RC", "RG"]
        },
        {
            'room': rooms[6],
            'round': 6,
            'teams': ["BF", "BI", "BO"]
        },
        {
            'room': rooms[6],
            'round': 7,
            'teams': ["RR", "RA", "RH"]
        },
        {
            'room': rooms[6],
            'round': 8,
            'teams': ["BP", "BE", "BL"]
        },
        {
            'room': rooms[6],
            'round': 9,
            'teams': ["RF", "RL", "RR"]
        },
        {
            'room': rooms[6],
            'round': 10,
            'teams': ["RO", "RQ", "RM"]
        },
        {
            'room': rooms[6],
            'round': 11,
            'teams': ["RB", "RK", "RQ"]
        },
        {
            'room': rooms[6],
            'round': 12,
            'teams': ["BM", "BE", "BI"]
        },

        {
            'room': rooms[7],
            'round': 1,
            'teams': ["RI", "RQ", "RA"]
        },
        {
            'room': rooms[7],
            'round': 2,
            'teams': ["BG", "BO", "BE"]
        },
        {
            'room': rooms[7],
            'round': 3,
            'teams': ["RG", "RO", "RB"]
        },
        {
            'room': rooms[7],
            'round': 4,
            'teams': ["BD", "BJ", "BP"]
        },
        {
            'room': rooms[7],
            'round': 5,
            'teams': ["RR", "RD", "RH"]
        },
        {
            'room': rooms[7],
            'round': 6,
            'teams': ["RG", "RI", "RK"]
        },
        {
            'room': rooms[7],
            'round': 7,
            'teams': ["RM", "RB", "RI"]
        },
        {
            'room': rooms[7],
            'round': 8,
            'teams': ["BQ", "BF", "BG"]
        },
        {
            'room': rooms[7],
            'round': 9,
            'teams': ["BA", "BC", "BE"]
        },
        {
            'room': rooms[7],
            'round': 10,
            'teams': ["BL", "BN", "BA"]
        },
        {
            'room': rooms[7],
            'round': 11,
            'teams': ["RC", "RL", "RR"]
        },
        {
            'room': rooms[7],
            'round': 12,
            'teams': ["BN", "BF", "BJ"]
        }]

    quizzes = []

    individuals = [['BA', 'Adam Greene'],
                   ['BA', 'Kari Greene'],
                   ['BB', 'David Castlebury'],
                   ['BB', 'Sawyer Castlebury'],
                   ['BC', 'Mark Crosby'],
                   ['BC', 'Esther Crosby'],
                   ['BD', 'Noah Crosby'],
                   ['BD', 'Logan Marunich'],
                   ['BE', 'James Ballinger'],
                   ['BE', 'Stevie Ballinger'],
                   ['BF', 'Lydia Ballinger'],
                   ['BF', 'Molly Carnell'],
                   ['BG', 'Walton Hunsader'],
                   ['BG', 'Micaiah Pipkin'],
                   ['BH', 'Brytni Castlebury'],
                   ['BH', 'Jodi Taylor'],
                   ['BI', 'Roger Greene'],
                   ['BI', 'Emma Carnell'],
                   ['BJ', 'Justus Wells'],
                   ['BJ', 'Landon Farmer'],
                   ['BK', 'Bethany Carnell'],
                   ['BK', 'Esther Tricquet'],
                   ['BL', 'Amaryssa Paige'],
                   ['BL', 'Landyn Marunich'],
                   ['BM', 'Abigail Unger'],
                   ['BM', 'Lydia Pipkin'],
                   ['BN', 'Gabriel Unger'],
                   ['BN', 'Ben Crosby'],
                   ['BO', 'Timothy Crosby'],
                   ['BO', 'Amelia Wells'],
                   ['BP', 'Eric Carnell'],
                   ['BP', 'Jonathan Carnell'],
                   ['BQ', 'Josiah Wells'],
                   ['BQ', 'Gabriel Ballinger'],
                   ['BR', 'Joshua Grimm'],
                   ['BR', 'Jonathan C Crosby'],
                   ['RA', 'Tammy Grimm'],
                   ['RA', 'Adam W '],
                   ['RB', 'Berean Cutler'],
                   ['RB', 'Breagan Cutler'],
                   ['RC', 'Emma Eastland'],
                   ['RC', 'Lydia Crosby'],
                   ['RD', 'Destiny Wells'],
                   ['RD', 'Bethany Cutler'],
                   ['RE', 'Paul Crosby'],
                   ['RE', 'Adam Eastlnd'],
                   ['RF', 'Samuel Unger'],
                   ['RF', 'Megan Carnell'],
                   ['RG', 'Charity Unger'],
                   ['RG', 'Rachel Carnell'],
                   ['RH', 'David Jones'],
                   ['RH', 'Jonah Unger'],
                   ['RI', 'James Crosby'],
                   ['RI', 'Joy Carnell'],
                   ['RJ', 'Abigail Greene'],
                   ['RJ', 'MaryGrace Carnell'],
                   ['RK', 'David Smith'],
                   ['RK', 'Matthew Crosby'],
                   ['RL', 'Brigitta Cutler'],
                   ['RL', 'Bellhannah Cutler'],
                   ['RM', 'Moriah Pipkin'],
                   ['RM', 'Grace Carnell'],
                   ['RN', 'Aimee Crosby'],
                   ['RN', 'Zachariah Crosby'],
                   ['RO', 'Joshua Unger'],
                   ['RO', 'Natalie Unger'],
                   ['RP', 'Chris Carnell'],
                   ['RP', 'Gloria Carnell'],
                   ['RQ', 'Miriam Carnell'],
                   ['RQ', 'Stephanie Farmer'],
                   ['RR', 'Josiah Ballinger'],
                   ['RR', 'Jaxon Wells'], ]

    team_memberships = []

    for individual in individuals:
        person = Individual.objects.create(name=individual[1],
                                           user=User.objects.create_user(individual[1], password="password"))
        team_memberships.append(TeamMembership(team=Team.objects.get(short_name=individual[0]), individual=person))

    TeamMembership.objects.bulk_create(team_memberships)

    def get_individual_by_name(name):
        try:
            return Individual.objects.get(name=name)
        except Individual.DoesNotExist:
            return Individual.objects.create(name=name,
                                             user=User.objects.create_user(name, password="password"))

    for match in matches:
        quiz = Quiz.objects.create(event=event, quizmaster=get_individual_by_name(match['room'][1]),
                                   scorekeeper=get_individual_by_name(match['room'][2]),
                                   room=match['room'][0], round=match['round'])
        for team in match['teams']:
            QuizParticipants.objects.create(quiz=quiz, team=Team.objects.get(short_name=team))

    # for room in rooms:
    #     # create users
    #
    #     for new_individual in room[1:]:
    #         get_individual_by_name(name=new_individual)
    #
    #     # add quizzes and questions per round
    #
    #     for round_num in range(1, NUM_ROUNDS + 1):
    #         quiz = Quiz.objects.create(event=event, quizmaster=get_individual_by_name(room[1]),
    #                                    scorekeeper=get_individual_by_name(room[2]), room=room[0], round=round_num)
    #         for question in range(1, 15 + 1):
    #             AskedQuestion.objects.create(quiz=quiz, question_number=question)

    return HttpResponse("Done")
