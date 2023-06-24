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
    teams = {

        "Grapes and Figs ": [
            "Abigail Unger",
            "Lydia Pipkin"
        ],
        "Opposites Attract ": [
            "Adam Greene",
            "Kari Greene"
        ],
        "_team-3_": [
            "James Crosby",
            "Joy Carnell"
        ],
        "The Apostle and The Regicide": [
            "Berean Cutler",
            "Breagan Cutler"
        ],
        "Serene Chaos": [
            "Brigitta Cutler",
            "Bellhannah Cutler"
        ],
        "_team-6_": [
            "Chris Carnell",
            "Gloria Carnell"
        ],
        "Truth-Seekers ": [
            "Jodi Taylor",
            "Brytni Castlebury"
        ],
        "_team-8_": [
            "David Castlebury",
            "Sawyer Castlebury"
        ],
        "David and Jonahthan": [
            "David Jones",
            "Jonah Unger"
        ],
        "_team-10_": [
            "David Smith",
            "Matthew Crosby"
        ],
        "Pearls of Grace ": [
            "Destiny Wells",
            "Bethany Cutler"
        ],
        "Sky's the Limit ": [
            "Emma Carnell",
            "Roger Greene"
        ],
        "Go Up Thou Bald Head": [
            "Eric Carnell",
            "Jonathan Carnell"
        ],
        "_team-14_": [
            "Esther Tricquet",
            "Bethany Carnell"
        ],
        "_team-15_": [
            "Gabriel Unger",
            "Ben Crosby"
        ],
        "Overwhelmingly Mediocre? ": [
            "James Ballinger",
            "Stevie Ballinger"
        ],
        "Sons of Thunder": [
            "Jonathan Crosby",
            "Paul Crosby"
        ],
        "_team-18_": [
            "Joshua Grimm",
            "Jonathan C Crosby"
        ],
        "_team-19_": [
            "Joshua Unger",
            "Natalie Unger"
        ],
        "Trailblazers ": [
            "Josiah Ballinger",
            "Jaxon Wells"
        ],
        "Torches ": [
            "Josiah Wells",
            "Gabriel Ballinger"
        ],
        "_team-22_": [
            "Justus Wells",
            "Landon Farmer"
        ],
        "_team-23_": [
            "Landyn Marunich",
            "Amaryssa Paige"
        ],
        "Smarties ": [
            "Lydia Ballinger",
            "Molly Carnell"
        ],
        "_team-25_": [
            "Mark Crosby",
            "Esther Crosby"
        ],
        "_team-26_": [
            "MaryGrace Carnell",
            "Abigail Greene"
        ],
        "_team-27_": [
            "Micaiah Pipkin",
            "Walton Hunsader"
        ],
        "Sinners with Pearls ": [
            "Miriam Carnell",
            "Stephanie Farmer"
        ],
        "_team-29_": [
            "Moriah Pipkin",
            "Grace Carnell"
        ],
        "_team-30_": [
            "Noah Crosby",
            "Logan Marunich"
        ],
        "_team-31_": [
            "Aimee Crosby",
            "Zachariah Crosby"
        ],
        "_team-32_": [
            "Rachel Carnell",
            "Charity Unger"
        ],
        "_team-33_": [
            "Samuel Unger",
            "Megan Carnell"
        ],
        "_team-34_": [
            "Sherri Crosby",
            "Tammy Grimm"
        ],
        "_team-35_": [
            "Timothy Crosby",
            "Amelia Wells"
        ],
        "Love is Blind ": [
            "Adam Eastland",
            "Emma Eastland"
        ],

    }
    season = Season.objects.first()
    organization = Organization.objects.first()
    event = Event.objects.get(pk=4)

    def get_team_by_name(team_name_str: str):
        try:
            return Team.objects.get(name=team_name_str)
        except (IntegrityError, Team.DoesNotExist):
            return Team.objects.create(name=team_name_str, organization=organization, season=season)

    def get_individual_by_name(name: str):
        try:
            return Individual.objects.get(name=name)
        except (IntegrityError, Individual.DoesNotExist):
            return Individual.objects.create(name=name, user=User.objects.create_user(name, password="password"))

    def get_team_membership(team_name_str: Team, individual: Individual):
        try:
            return TeamMembership.objects.get(team=team_name_str, individual=individual)
        except (IntegrityError, TeamMembership.DoesNotExist):
            return TeamMembership.objects.create(team=team_name_str, individual=individual)

    for team_name, team in zip(teams.keys(), teams.values()):
        new_team = get_team_by_name(team_name.strip())
        new_individuals = [
            get_individual_by_name(individual.strip()) for
            individual in team]
        [get_team_membership(new_team, individual) for individual in
         new_individuals]

    rooms = [
        ['A', "Nathan Crosby", "Abigail Crosby"],
        ['B', "Jim Cutler", "Jacqueline Cutler"],
        ['C', "Daniel Jones", "Debbie Eastland"],
        ['D', "Daniel Crosby", "Victoria Eastland"],
        ['E', "Heather Crosby", "Lydia Crosby"],
        ['F', "Michael Jones", "Danielle Crosby"],
        ['G', "Adam Eastland", "Emma Eastland"]
    ]

    NUM_ROUNDS = 12

    def get_individual_by_name(name):
        try:
            return Individual.objects.get(name=name)
        except Individual.DoesNotExist:
            Individual.objects.create(name=new_individual,
                                      user=User.objects.create_user(new_individual, password="password"))

    for room in rooms:
        # create users

        for new_individual in room[1:]:
            get_individual_by_name(name=new_individual)

        # add quizzes and questions per round

        for round_num in range(1, NUM_ROUNDS + 1):
            quiz = Quiz.objects.create(event=event, quizmaster=get_individual_by_name(room[1]),
                                       scorekeeper=get_individual_by_name(room[2]), room=room[0], round=round_num)
            for question in range(1, 15 + 1):
                AskedQuestion.objects.create(quiz=quiz, question_number=question)

    return HttpResponse("Done")
