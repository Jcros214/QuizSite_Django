from typing import List, Dict, Tuple, Optional

from django.db import transaction

from TournamentManager.initial_data.current.data import quizzes, rooms, divisions, progressions, quizzes_afternoon2, \
    quizzes_afternoon3
from Records.models import *


def individual_by_name(name) -> Individual:
    if Individual.objects.filter(name=name).exists():
        return Individual.objects.get(name=name)
    else:
        user = User.objects.create_user(username=name, password='secure')
        individual = Individual.objects.create(name=name, user=user)

        return individual


def league_by_name(name) -> League:
    if League.objects.filter(name=name).exists():
        return League.objects.get(name=name)
    else:
        return League.objects.create(name=name)


def get_season_by_args(start_date='2023-07-15', material='Matthew 5-7', league=None) -> Season:
    if league is None:
        league = League.objects.get(name='GAQSS')

    season_query = Season.objects.filter(start_date=start_date, material=material, league=league)

    if season_query.exists():
        return season_query.first()
    else:
        return Season.objects.create(start_date=start_date, material=material, league=league)


def get_event_by_args(date, season, location, **kwargs) -> Event:
    event_query = Event.objects.filter(date=date, season=season, location=location, **kwargs)

    return event_query.first() if event_query.exists() else Event.objects.create(date=date, season=season,
                                                                                 location=location)


def get_organization_by_args(name, short_name, address) -> Organization:
    organization_query = Organization.objects.filter(name=name, short_name=short_name, address=address)
    return organization_query.first() if organization_query.exists() \
        else Organization.objects.create(name=name, short_name=short_name, address=address)


def get_division_by_args(name, event) -> Division:
    division_query = Division.objects.filter(name=name, event=event)

    return division_query.first() if division_query.exists() else Division.objects.create(name=name, event=event)


LOCATION = get_organization_by_args(name='Faith Baptist Church', short_name='Faith',
                                    address='500 W. Lee Road in Taylors SC 29687')
LEAGUE = league_by_name('GAQSS')
SEASON = get_season_by_args(league=LEAGUE)
MORNING_EVENT = Event.objects.create(date='2023-07-15', season=SEASON, location=LOCATION)
AFTERNOON_EVENT1 = Event.objects.create(date='2023-07-15', season=SEASON, location=LOCATION, isTournament=False)
AFTERNOON_EVENT2 = Event.objects.create(date='2023-07-15', season=SEASON, location=LOCATION, isTournament=True)


# @transaction.atomic
def preload_spectacular_event():
    new_teams = []
    new_individuals = []
    new_team_memberships = []

    for division_name, division_teams in divisions.items():
        division_object = get_division_by_args(name=division_name, event=MORNING_EVENT)

        for short_name, team in division_teams.items():
            team_object = Team.objects.create(name=team[0], organization=LOCATION, season=SEASON,
                                              short_name=(division_name + short_name), type=team[1])

            division_object.teams.add(team_object)

            individuals = team[2]

            new_individuals += [Individual(name=individuals[0], gender=individuals[1]),
                                Individual(name=individuals[2], gender=individuals[3])]

            for individual in new_individuals[-2:]:
                new_team_memberships.append(TeamMembership(team=team_object, individual=individual))

    # print(new_teams, new_individuals, new_team_memberships)

    Individual.objects.bulk_create(new_individuals)
    Team.objects.bulk_create(new_teams)
    TeamMembership.objects.bulk_create(new_team_memberships)

    _MORNING_SCHEDULE: Dict[Tuple[str, int], Tuple[Tuple[str, str, str]]] = quizzes

    '''
    Ex Morning Schedule:
    
    _MORNING_SCHEDULE = {
        'A': [[ 'RA',  'RB',  'RC'], [ 'RD',  'RE',  'RF'], ...],
        'B': [['...', '...', '...'], ['...', '...', '...'], ...],
        'C': [['...', '...', '...'], ['...', '...', '...'], ...],
        'D': [['...', '...', '...'], ['...', '...', '...'], ...],
        'E': [['...', '...', '...'], ['...', '...', '...'], ...],
        'F': [['...', '...', '...'], ['...', '...', '...'], ...],
        'G': [['...', '...', '...'], ['...', '...', '...'], ...],
    }
    '''

    # list(Room.objects.all())
    # [Room(event=MORNING_EVENT, name=room_name, quizmaster=individual_by_name(rooms[room_name][0]),
    #       scorekeeper=individual_by_name(rooms[room_name][1])) for room_name in rooms]

    new_rooms = []

    for event in [MORNING_EVENT, AFTERNOON_EVENT1, AFTERNOON_EVENT2]:
        for room_name in rooms.keys():
            new_rooms += [Room(event=event, name=room_name, quizmaster=individual_by_name(rooms[room_name][0]),
                               scorekeeper=individual_by_name(rooms[room_name][1]))]
    Room.objects.bulk_create(new_rooms)

    MORNING_QUIZZES = []
    MORNING_QUESTIONS = []
    MORNING_QUIZPARTICIPANTS = []

    for room, rounds in _MORNING_SCHEDULE.items():
        room = Room.objects.get(name=room, event=MORNING_EVENT)
        for round_num, quiz in enumerate(rounds):
            MORNING_QUIZZES.append(
                Quiz(event=MORNING_EVENT, room=room, round=round_num + 1, allow_ties=True, type='normal'))

            if len(quiz) != 3:
                continue

            MORNING_QUIZPARTICIPANTS += [
                QuizParticipants(quiz=MORNING_QUIZZES[-1], team=Team.objects.get(short_name=short_name))
                for short_name in quiz
            ]

            MORNING_QUESTIONS += [AskedQuestion(quiz=MORNING_QUIZZES[-1], question_number=q_num, type='normal')
                                  for q_num in range(1, 16)]

    for quiz_event in [(quizzes_afternoon2, AFTERNOON_EVENT1), (quizzes_afternoon3, AFTERNOON_EVENT2)]:
        event = quiz_event[1]
        for quiz_dict in quiz_event[0]:
            quiz_room = Room.objects.get(name=quiz_dict[0], event=event)
            MORNING_QUIZZES.append(
                Quiz(event=quiz_event[1], room=quiz_room,
                     round=quiz_dict[1], allow_ties=True, type='normal'))

    Quiz.objects.bulk_create(MORNING_QUIZZES)
    AskedQuestion.objects.bulk_create(MORNING_QUESTIONS)
    QuizParticipants.objects.bulk_create(MORNING_QUIZPARTICIPANTS)
    #
    # '''
    # Ex AFTERNOON Schedule:
    #
    # _AFTERNOON_SCHEDULE = {
    #     'A': [[], [], [], [],   ...],
    #     'B': [[], [], [], [],   ...],
    #     'C': [[], [], [],       ...],
    #     'D': [[], [], [],       ...],
    #     'E': [[], [],           ...],
    #     'F': [[], [],           ...],
    #     'G': [[], [],           ...],
    # }
    # '''
    #
    # AFTERNOON_EVENT = Event.objects.create(date='2023-07-15', season=SEASON, location=LOCATION, isTournament=True)
    # AFTERNOON_ROOMS = Room.objects.bulk_create(
    #     [Room(event=AFTERNOON_EVENT, name=room[0], quizmaster=individual_by_name(room[1]),
    #           scorekeeper=individual_by_name(room[1])) for room in rooms]
    # )
    #
    # AFTERNOON_QUIZZES = []
    # AFTERNOON_QUESTIONS = []
    # # AFTERNOON_QUIZPARTICIPANTS = []
    #
    # for room, rounds in _AFTERNOON_SCHEDULE.items():
    #     for round_num, quiz in enumerate(rounds):
    #         AFTERNOON_QUIZZES.append(Quiz(event=AFTERNOON_EVENT, room=room, round=round_num))
    #         AFTERNOON_QUESTIONS += [AskedQuestion(quiz=AFTERNOON_QUIZZES[-1], question_number=q_num)
    #                                 for q_num in range(1, 16)]
    #
    #         # AFTERNOON_QUIZPARTICIPANTS += [
    #         #     QuizParticipants(quiz=AFTERNOON_QUIZZES[-1], team=Team.objects.get(short_code=short_code))
    #         #     for short_code in quiz
    #         # ]
    #
    # with transaction.atomic():
    #     Quiz.objects.bulk_create(AFTERNOON_QUIZZES)
    #     AskedQuestion.objects.bulk_create(AFTERNOON_QUESTIONS)
    #     # QuizParticipants.objects.bulk_create(AFTERNOON_QUIZPARTICIPANTS)

    division_names = [
        'Championship',
        'Consolation 1',
        'Consolation 2',
        'Consolation 3',
    ]

    new_divisions = []

    for event in [AFTERNOON_EVENT1, AFTERNOON_EVENT2]:
        for division_name in division_names:
            new_divisions += [Division(event=event, name=division_name)]

    Division.objects.bulk_create(new_divisions)

    # Create Progressions
    new_progressions = []

    for progression in progressions:
        prog_type = progression['type']
        prog_quiz = Quiz.objects.get(id=progression['quiz']) if progression['quiz'] else None
        prog_division = Division.objects.get(id=progression['division']) if progression['division'] else None
        prog_rank = progression['rank']
        prog_next_quiz = Quiz.objects.get(id=progression['next_quiz'])
        prog_next_division = Division.objects.get(id=progression['next_division']) if progression[
            'next_division'] else None
        prog_isCompleted = progression['isCompleted']
        prog_allow_ties = progression['allow_ties']

        new_progressions += [QuizProgression(
            type=prog_type,
            quiz=prog_quiz,
            division=prog_division,
            rank=prog_rank,
            next_quiz=prog_next_quiz,
            next_division=prog_next_division,
            isCompleted=prog_isCompleted,
            allow_ties=prog_allow_ties
        )]

    QuizProgression.objects.bulk_create(new_progressions)
