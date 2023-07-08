from django.apps import apps

####################################################################################################
####################################################################################################
# Import Data
from typing import Dict, List

from django.db import transaction

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
    'RE': ['Brothers of Lightning', 'Friend', ['Paul Crosby', True, 'Adam Eastland', True]],
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

afternoon_progressions = ...
#
####################################################################################################
####################################################################################################


Organization = apps.get_model('Records', 'Organization')
League = apps.get_model('Records', 'League')
LeagueMembership = apps.get_model('Records', 'LeagueMembership')
Individual = apps.get_model('Records', 'Individual')
Season = apps.get_model('Records', 'Season')
Team = apps.get_model('Records', 'Team')
TeamMembership = apps.get_model('Records', 'TeamMembership')
Event = apps.get_model('Records', 'Event')
Room = apps.get_model('Records', 'Room')
Quiz = apps.get_model('Records', 'Quiz')
QuizParticipants = apps.get_model('Records', 'QuizParticipants')
AskedQuestion = apps.get_model('Records', 'AskedQuestion')
QuizProgression = apps.get_model('Records', 'QuizProgression')


def individual_by_name(name):
    if Individual.objects.filter(name=name).exists():
        return Individual.objects.get(name=name)
    else:
        return Individual.objects.create(name=name)


def preload_spectacular_event():
    LEAGUE = League.objects.create(name='GAQSS')

    SEASON = Season.objects.create(start_date='2023-07-15', material='Matthew 5-7', league=LEAGUE)

    # Add teams

    LOCATION = Organization.objects.create(name='Church', short_name='Church', address='1234 Church St')

    _MORNING_SCHEDULE: Dict[str, List[List[str, str, str]]] = {room[0]: [] for room in rooms}
    _AFTERNOON_SCHEDULE: Dict[str, List[List[str, str, str]]] = {room[0]: [] for room in rooms}

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

    MORNING_EVENT: Event = Event.objects.create(date='2023-07-15', season=SEASON, location=LOCATION)
    MORNING_ROOMS: List[Room] = Room.objects.bulk_create(
        [Room(event=MORNING_EVENT, name=room[0], quizmaster=individual_by_name(room[1]),
              scorekeeper=individual_by_name(room[1])) for room in rooms]
    )

    MORNING_QUIZZES = []
    MORNING_QUESTIONS = []
    MORNING_QUIZPARTICIPANTS = []

    for room, rounds in _MORNING_SCHEDULE.items():
        for round_num, quiz in enumerate(rounds):
            MORNING_QUIZZES.append(Quiz(event=MORNING_EVENT, room=room, round=round_num))

            MORNING_QUIZPARTICIPANTS += [
                QuizParticipants(quiz=MORNING_QUIZZES[-1], team=Team.objects.get(short_code=short_code))
                for short_code in quiz
            ]

            MORNING_QUESTIONS += [AskedQuestion(quiz=MORNING_QUIZZES[-1], question_number=q_num)
                                  for q_num in range(1, 16)]

    with transaction.atomic():
        Quiz.objects.bulk_create(MORNING_QUIZZES)
        AskedQuestion.objects.bulk_create(MORNING_QUESTIONS)
        QuizParticipants.objects.bulk_create(MORNING_QUIZPARTICIPANTS)

    '''
    Ex AFTERNOON Schedule:

    _AFTERNOON_SCHEDULE = {
        'A': [[], [], [], [],   ...],
        'B': [[], [], [], [],   ...],
        'C': [[], [], [],       ...],
        'D': [[], [], [],       ...],
        'E': [[], [],           ...],
        'F': [[], [],           ...],
        'G': [[], [],           ...],
    }
    '''

    AFTERNOON_EVENT = Event.objects.create(date='2023-07-15', season=SEASON, location=LOCATION, isTournament=True)
    AFTERNOON_ROOMS = Room.objects.bulk_create(
        [Room(event=AFTERNOON_EVENT, name=room[0], quizmaster=individual_by_name(room[1]),
              scorekeeper=individual_by_name(room[1])) for room in rooms]
    )

    AFTERNOON_QUIZZES = []
    AFTERNOON_QUESTIONS = []
    # AFTERNOON_QUIZPARTICIPANTS = []

    for room, rounds in _AFTERNOON_SCHEDULE.items():
        for round_num, quiz in enumerate(rounds):
            AFTERNOON_QUIZZES.append(Quiz(event=AFTERNOON_EVENT, room=room, round=round_num))
            AFTERNOON_QUESTIONS += [AskedQuestion(quiz=AFTERNOON_QUIZZES[-1], question_number=q_num)
                                    for q_num in range(1, 16)]

            # AFTERNOON_QUIZPARTICIPANTS += [
            #     QuizParticipants(quiz=AFTERNOON_QUIZZES[-1], team=Team.objects.get(short_code=short_code))
            #     for short_code in quiz
            # ]

    with transaction.atomic():
        Quiz.objects.bulk_create(AFTERNOON_QUIZZES)
        AskedQuestion.objects.bulk_create(AFTERNOON_QUESTIONS)
        # QuizParticipants.objects.bulk_create(AFTERNOON_QUIZPARTICIPANTS)
