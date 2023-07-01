# from django.db import IntegrityError
# from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import transaction

from .round_robin_scheduler import RoundRobinScheduler, tabulate_rounds, find_fairness
from django.contrib.auth.decorators import user_passes_test

# from django.contrib.auth.models import User
from django.contrib.auth.models import Group

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


@user_passes_test(lambda u: u.is_superuser)
def populate_round_robbin_event(request):
    if request.method != 'POST':
        return render(request, 'Manager/round_robin_event_maker.html')

    # season = request.POST.get("season")
    # teams = request.POST.get("teams")
    # event = request.POST.get("event")
    # TODO: TMP; RM
    season = Season.objects.first()
    organization = Organization.objects.first()
    event = Event.objects.create(date="2023-07-01", season=season, location=organization)

    rooms = [
        ['A', 'Nathan Crosby', 'Debbie Eastland'],
        ['B', 'Jim Cutler', 'Jacqueline Cutler'],
        ['C', 'Daniel Crosby', 'Victoria Eastland'],
        ['D', 'Daniel Jones', 'Sherri Crosby'],
        ['E', 'Heather Crosby', 'David Crosby'],
        ['F', 'Michael Jones', 'Hannah Grimm'],
        ['G', 'Austin Handal', 'Sarah Handal']
    ]

    new_matches = {'A1': ['RB', 'RJ', 'RR'],
                   'A2': ['BH', 'BP', 'BF'],
                   'A3': ['RH', 'RP', 'RC'],
                   'A4': ['BE', 'BK', 'BQ'],
                   'A5': ['RM', 'RE', 'RI'],
                   'A6': ['BA', 'BJ', 'BP'],
                   'A7': ['RN', 'RC', 'RJ'],
                   'A8': ['RB', 'RD', 'RF'],
                   'A9': ['RA', 'RG', 'RM'],
                   'A10': ['BG', 'BO', 'BB'],
                   'A11': ['RD', 'RG', 'RM'],
                   'A12': ['RN', 'RP', 'RR'],
                   'B1': ['RC', 'RK', 'RM'],
                   'B2': ['RL', 'RH', 'RJ'],
                   'B3': ['RI', 'RQ', 'RD'],
                   'B4': ['BF', 'BL', 'BR'],
                   'B5': ['RN', 'RF', 'RJ'],
                   'B6': ['BB', 'BK', 'BQ'],
                   'B7': ['RO', 'RD', 'RK'],
                   'B8': ['BR', 'BA', 'BH'],
                   'B9': ['RB', 'RH', 'RN'],
                   'B10': ['BH', 'BP', 'BC'],
                   'B11': ['RE', 'RH', 'RN'],
                   'B12': ['BO', 'BA', 'BK'],
                   'C1': ['RD', 'RL', 'RN'],
                   'C2': ['BI', 'BQ', 'BA'],
                   'C3': ['RJ', 'RR', 'RE'],
                   'C4': ['RA', 'RC', 'RE'],
                   'C5': ['BN', 'BP', 'BR'],
                   'C6': ['BC', 'BL', 'BR'],
                   'C7': ['RP', 'RE', 'RL'],
                   'C8': ['BM', 'BB', 'BI'],
                   'C9': ['RC', 'RI', 'RO'],
                   'C10': ['BI', 'BQ', 'BD'],
                   'C11': ['RF', 'RI', 'RO'],
                   'C12': ['BP', 'BB', 'BL'],
                   'D1': ['RE', 'RG', 'RO'],
                   'D2': ['BJ', 'BR', 'BB'],
                   'D3': ['RK', 'RM', 'RF'],
                   'D4': ['BA', 'BG', 'BM'],
                   'D5': ['RO', 'RA', 'RK'],
                   'D6': ['BD', 'BG', 'BM'],
                   'D7': ['RQ', 'RF', 'RG'],
                   'D8': ['BN', 'BC', 'BJ'],
                   'D9': ['RD', 'RJ', 'RP'],
                   'D10': ['BJ', 'BR', 'BE'],
                   'D11': ['BG', 'BI', 'BK'],
                   'D12': ['BQ', 'BC', 'BG'],
                   'E1': ['RF', 'RH', 'RP'],
                   'E2': ['BK', 'BM', 'BC'],
                   'E3': ['BO', 'BQ', 'BM'],
                   'E4': ['BB', 'BH', 'BN'],
                   'E5': ['RP', 'RB', 'RL'],
                   'E6': ['BE', 'BH', 'BN'],
                   'E7': ['BB', 'BD', 'BF'],
                   'E8': ['BO', 'BD', 'BK'],
                   'E9': ['RE', 'RK', 'RQ'],
                   'E10': ['BK', 'BM', 'BF'],
                   'E11': ['RA', 'RJ', 'RP'],
                   'E12': ['BR', 'BD', 'BH'],
                   'F1': ['BL', 'BH', 'BJ'],
                   'F2': ['BL', 'BN', 'BD'],
                   'F3': ['RL', 'RN', 'RA'],
                   'F4': ['BC', 'BI', 'BO'],
                   'F5': ['RQ', 'RC', 'RG'],
                   'F6': ['BF', 'BI', 'BO'],
                   'F7': ['RR', 'RA', 'RH'],
                   'F8': ['BP', 'BE', 'BL'],
                   'F9': ['RF', 'RL', 'RR'],
                   'F10': ['RO', 'RQ', 'RM'],
                   'F11': ['RB', 'RK', 'RQ'],
                   'F12': ['BM', 'BE', 'BI'],
                   'G1': ['RI', 'RQ', 'RA'],
                   'G2': ['BG', 'BO', 'BE'],
                   'G3': ['RG', 'RO', 'RB'],
                   'G4': ['BD', 'BJ', 'BP'],
                   'G5': ['RR', 'RD', 'RH'],
                   'G6': ['RG', 'RI', 'RK'],
                   'G7': ['RM', 'RB', 'RI'],
                   'G8': ['BQ', 'BF', 'BG'],
                   'G9': ['BA', 'BC', 'BE'],
                   'G10': ['BL', 'BN', 'BA'],
                   'G11': ['RC', 'RL', 'RR'],
                   'G12': ['BN', 'BF', 'BJ'],

                   }

    afternoon_matches = (('A13', ('R2', 'R3', 'B5')),
                         ('A14', ('R1', 'R4', 'B6')),
                         ('A15', ('HA1', 'MB1', 'MA2')),
                         ('A16', ('HA2', 'HB3', 'MA3')),
                         ('A17', ('HA4/HB4', 'MA4', 'MB4')),
                         ('A18', ('HA4/HB4', 'HA5', 'MA5')),
                         ('A19', ('HA6', 'MA6')),  # 2-team match
                         ('B13', ('B2', 'B3', 'R5')),
                         ('B14', ('B1', 'B4', 'R6')),
                         ('B15', ('HB1', 'MA1', 'MB2')),
                         ('B16', ('HB2', 'HA3', 'MB3')),
                         ('C13', ('R8', 'R9', 'B11')),
                         ('C14', ('R7', 'R10', 'B12')),
                         ('C15', ('HC1', 'MD1', 'MC2')),
                         ('C16', ('HC2', 'HD3', 'MC3')),
                         ('C17', ('HC4/HD4', 'MC4', 'MD4')),
                         ('C18', ('HC4/HD4', 'HC5', 'MC5')),
                         ('C19', ('HC6', 'MC6')),  # 2-team match
                         ('D13', ('B8', 'B9', 'R11')),
                         ('D14', ('B7', 'B10', 'R12')),
                         ('D15', ('HD1', 'MC1', 'MD2')),
                         ('D16', ('HD2', 'HC3', 'MD3')),
                         ('E13', ('B14', 'B16', 'R17')),
                         ('E14', ('R13', 'HG1', 'MF1')),
                         ('E15', ('HE2', 'MF2', 'MG2')),
                         ('E16', ('HE3/HF3', 'ME3', 'MF3')),
                         ('E17', ('HE3/HF3', 'HE4', 'ME4')),
                         ('E18', ('HE5', 'ME5')),  # 2-team match
                         ('F13', ('R15', 'B17', 'R18')),
                         ('F14', ('B13', 'HF1', 'ME1')),
                         ('F15', ('HF2', 'HG2', 'ME2')),
                         ('G13', ('B15', 'R16', 'B18')),
                         ('G14', ('R14', 'HE1', 'MG1')),)

    teams = {
        'BA': ['Taking no Thought', 'Sibling', ['Bethany Carnell', False, 'Esther Tricquet', False]],

        'BB': ['Go Up Thou Bald Head', 'Sibling', ['Eric Carnell', True, 'Jonathan Carnell', True]],

        'BC': ['Once Upon a Quiz', 'Couple', ['Mark Crosby', True, 'Esther Crosby', False]],

        'BD': ['Baby G and Big B', 'Friend', ['Gabriel Unger', True, 'Ben Crosby', True]],

        'BE': ['A City on a Hill', 'Friend', ['Justus Wells', True, 'Landon Farmer', True]],

        'BF': ['Grapes and Figs', 'Friend', ['Abigail Unger', False, 'Lydia Pipkin', False]],

        'BG': ['Sword of the Spirit Brothers', 'Friend', ['Walton Hunsader', True, 'Micaiah Pipkin', True]],

        'BH': ['Truth-Seekers', 'Friend', ['Brytni Castlebury', False, 'Jodi Taylor', False]],

        'BI': ['Sky\'s the Limit', 'Friend', ['Roger Greene', True, 'Emma Carnell', False]],

        'BJ': ['Mr. and Mrs. B', 'Couple', ['James Ballinger', True, 'Stevie Ballinger', False]],

        'BK': ['Opposites Attract', 'Couple', ['Adam Greene', True, 'Kari Greene', False]],

        'BL': ['the L.A.M.P.s', 'Friend', ['Amaryssa Paige', False, 'Landyn Marunich', True]],

        'BM': ['Cheese and Crackers', 'Friend', ['Lydia Ballinger', False, 'Molly Carnell', False]],

        'BN': ['Prime Time', 'Friend', ['Noah Crosby', True, 'Logan Marunich', True]],

        'BO': ['Artsy Smartsy', 'Friend', ['Timothy Crosby', True, 'Amelia Wells', False]],

        'BP': ['Him That Knocketh Again', 'Friend', ['Elijah Crosby', True, 'Jason Farmer', True]],

        'BQ': ['Torches', 'Friend', ['Josiah Wells', True, 'Gabriel Ballinger', True]],

        'BR': ['Savory Salt', 'Cousin', ['Joshua Grimm', True, 'Jonathan C Crosby', True]],

        'RA': ['mg squared', 'Friend', ['Moriah Pipkin', False, 'Grace Carnell', False]],

        'RB': ['David and Jonahthan', 'Friend', ['David Jones', True, 'Jonah Unger', True]],

        'RC': ['Lyds and Pants', 'Friend', ['Emma Eastland', False, 'Lydia Crosby', False]],

        'RD': ['Mountain Men', 'Friend', ['David Smith', True, 'Matthew Crosby', True]],

        'RE': ['Brothers of Lightning', 'Friend', ['Paul Crosby', True, 'Adam Eastlnd', True]],

        'RF': ['The Attaining Twain', 'Friend', ['Samuel Unger', True, 'Megan Carnell', False]],

        'RG': ['No stinkin’ thinkin’', 'Parent/Child', ['Charity Unger', False, 'Rachel Carnell', False]],

        'RH': ['The Apostle and The Regicide', 'Sibling', ['Berean Cutler', True, 'Breagan Cutler', True]],

        'RI': ['JC x 4', 'Cousin', ['James Crosby', True, 'Joy Carnell', False]],

        'RJ': ['Grace and Joy', 'Friend', ['Abigail Greene', False, 'MaryGrace Carnell', False]],

        'RK': ['Pearls of Grace', 'Friend', ['Destiny Wells', False, 'Bethany Cutler', False]],

        'RL': ['Serene Chaos', 'Sibling', ['Brigitta Cutler', False, 'Bellhannah Cutler', False]],

        'RM': ['Joyful Pilgrims', 'Friend', ['Tammy Grimm', False, 'Adam Wells', False]],

        'RN': ['Peacemakers', 'Parent/Child', ['Aimee Crosby', True, 'Zachariah Crosby', True]],

        'RO': ['Married yet Single', 'Couple', ['Joshua Unger', True, 'Natalie Unger', False]],

        'RP': ['Wash Thy Face', 'Parent/Child', ['Chris Carnell', True, 'Gloria Carnell', False]],

        'RQ': ['Sinners with Pearls', 'Friend', ['Miriam Carnell', False, 'Stephanie Farmer', False]],

        'RR': ['Trailblazers', 'Friend', ['Josiah Ballinger', False, 'Jaxon Wells', False]],

    }

    team_memberships = []

    user_objects = []
    individuals_objects = []
    team_objects = []
    team_memberships_objects = []

    for team_code, team in teams.items():
        if Team.objects.filter(short_name=team_code).exists():
            Team.objects.filter(short_name=team_code).delete()

        team_objects.append(
            Team(short_name=team_code, name=team[0], organization=organization, season=season, division=team_code[0],
                 type=team[1]))

        for individual_name in team[2]:

            if individual_name in (False, True):
                individuals_objects[-1].gender = individual_name

            if User.objects.filter(username=individual_name).exists():
                user = User.objects.get(username=individual_name)
            else:
                user = User.objects.create_user(username=individual_name, password="password")

            if Individual.objects.filter(name=individual_name).exists():
                Individual.objects.filter(name=individual_name).delete()

            individuals_objects.append(Individual(name=individual_name, user=user))

        team_memberships_objects += [TeamMembership(team=team_objects[-1], individual=individuals_objects[-_]) for _ in
                                     range(1, 3)]

    with transaction.atomic():
        User.objects.bulk_create(user_objects)
        Individual.objects.bulk_create(individuals_objects)
        Team.objects.bulk_create(team_objects)
        TeamMembership.objects.bulk_create(team_memberships_objects)

    old_quizzes = Quiz.objects.filter(event=event)

    if old_quizzes.exists():
        old_quizzes.delete()

    # create users
    # create individuals
    # create quizzes

    user_objects = []
    individuals_objects = []
    quiz_objects = []
    asked_question_objects = []
    quiz_participant_objects = []

    scorekeeper_group = Group.objects.get(name='scorekeeper')
    quizmaster_group = Group.objects.get(name='quizmaster')

    for room in rooms:
        for individual_name in room[1:]:
            if User.objects.filter(username=individual_name).exists():
                user = User.objects.get(username=individual_name)
            else:
                user = User.objects.create_user(username=individual_name, password="secret")

            if Individual.objects.filter(name=individual_name).exists():
                Individual.objects.filter(name=individual_name).delete()

            individuals_objects.append(Individual(name=individual_name, user=user))

        quizmaster = individuals_objects[-2]
        scorekeeper = individuals_objects[-1]

        # scorekeeper_group.user_set.add(scorekeeper.user)
        # quizmaster_group.user_set.add(quizmaster.user)

        for rnd in range(1, 12 + 1):
            quiz_objects.append(
                Quiz(event=event, quizmaster=quizmaster, scorekeeper=scorekeeper, room=room[0], round=rnd))

            asked_question_objects += [
                AskedQuestion(quiz=quiz_objects[-1], question_number=question_num) for question_num in range(1, 15 + 1)]

            quiz_participant_objects += [
                QuizParticipants(quiz=quiz_objects[-1], team=Team.objects.get(short_name=team_code)) for team_code in
                new_matches[f"{room[0]}{rnd}"]]

    with transaction.atomic():
        User.objects.bulk_create(user_objects)
        Individual.objects.bulk_create(individuals_objects)
        Quiz.objects.bulk_create(quiz_objects)
        QuizParticipants.objects.bulk_create(quiz_participant_objects)
        AskedQuestion.objects.bulk_create(asked_question_objects)

    user_objects = []
    individuals_objects = []
    quiz_objects = []
    quiz_participant_objects = []
    asked_question_objects = []

    afternoon_event = Event.objects.create(date=event.date, season=event.season, location=event.location,
                                           isTournament=True)

    for match in afternoon_matches:
        room = {
            'A': rooms[0],
            'B': rooms[1],
            'C': rooms[2],
            'D': rooms[3],
            'E': rooms[4],
            'F': rooms[5],
            'G': rooms[6],
        }[match[0][0]]

        quizmaster_name = room[1]
        scorekeeper_name = room[2]

        quizmaster = Individual.objects.get(name=quizmaster_name)
        scorekeeper = Individual.objects.get(name=scorekeeper_name)

        quiz_objects.append(
            Quiz(event=afternoon_event, quizmaster=quizmaster, scorekeeper=scorekeeper, room=room[0],
                 round=match[0][1:]))

        asked_question_objects += [
            AskedQuestion(quiz=quiz_objects[-1], question_number=question_num) for question_num in range(1, 15 + 1)]
        #
        # quiz_participant_objects += [
        #     QuizParticipants(quiz=quiz_objects[-1], team=Team.objects.get(short_name=team_code)) for team_code in
        #     match[1:]]

    with transaction.atomic():
        User.objects.bulk_create(user_objects)
        Individual.objects.bulk_create(individuals_objects)
        Quiz.objects.bulk_create(quiz_objects)
        QuizParticipants.objects.bulk_create(quiz_participant_objects)
        AskedQuestion.objects.bulk_create(asked_question_objects)

    for user in User.objects.order_by('-id')[:len(user_objects)]:
        user.set_password("secret")
        user.save()
    return redirect('/')
