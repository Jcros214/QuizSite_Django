from typing import Optional, Dict, Tuple, List, Union, Any

from django.core.exceptions import ImproperlyConfigured
from django.db import models

from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.db import connection


# from django.utils.functional import SimpleLazyObject


class Organization(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class League(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class LeagueMembership(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.organization.name} - {self.league.name}"


class Individual(models.Model):
    MALE = True
    FEMALE = False

    name = models.CharField(max_length=100, unique=True)
    birthday = models.DateField("", auto_now=False, auto_now_add=False, default=None, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    gender = models.BooleanField(choices=((MALE, "Male"), (FEMALE, "Female")), null=True, blank=True)

    def __str__(self):
        return self.name


class Season(models.Model):
    start_date = models.DateField("", auto_now=False, auto_now_add=False)
    material = models.CharField(max_length=100)
    league = models.ForeignKey(League, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.league} - {self.start_date.year}"

    def get_teams(self):
        return Team.objects.filter(season_id=self.pk)

    def get_individuals(self):
        return Individual.objects.filter(teammembership__team__season_id=self.pk).distinct()


class Team(models.Model):
    class Meta:
        unique_together = (('name', 'organization', 'season'), ('short_name', 'season'))

    name = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    short_name = models.CharField(max_length=20, blank=True, null=True)

    type = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.short_name

    def __repr__(self):
        return f"<Team {self.short_name}>"

    def try_short_name(self):
        if self.short_name:
            return self.short_name
        else:
            return self.name

    def isMember(self, individual):
        if individual:
            return TeamMembership.objects.filter(team_id=self.pk, individual_id=individual.pk).exists()
        else:
            return False

    def get_absolute_url(self):
        return f"/records/{self.season.league.pk}/{self.season.pk}/team/{self.pk}"

    def get_individuals(self):
        return Individual.objects.filter(teammembership__team_id=self.pk)


class TeamMembership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    individual = models.ForeignKey(Individual, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.team.name} - {self.individual.name}"


class Event(models.Model):
    # name = models.CharField(max_length=100)
    date = models.DateField("", auto_now=False, auto_now_add=False)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    location = models.ForeignKey(Organization, on_delete=models.CASCADE)

    isTournament = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.season} - {'afternoon' if self.isTournament else 'morning'}"

    def get_team_rank(self, team: Team):
        teams = sorted(self.season.get_teams(), key=lambda t: self.get_team_score(t), reverse=True)

        if team in teams:
            return teams.index(team) + 1
        else:
            return None

    def get_team_score(self, team: Team):
        individuals = Individual.objects.filter(teammembership__team=team)
        questions = AskedQuestion.objects.filter(quiz__event_id=self.pk, individual__in=individuals)

        return sum([q.value for q in questions])

    def get_individual_score(self, individual: Individual):
        return sum([q.value for q in AskedQuestion.objects.filter(quiz__event_id=self.pk, individual=individual)])

    def get_team_current_quiz(self, team: Team):
        participants = QuizParticipants.objects.filter(team=team, quiz__event_id=self.pk)
        return Quiz.objects.filter(quizparticipants__in=participants).filter(isValidated=False).order_by(
            'round').first()

    def get_team_next_quiz(self, team: Team):
        participants = QuizParticipants.objects.filter(team=team, quiz__event_id=self.pk)
        return Quiz.objects.filter(quizparticipants__in=participants).filter(isValidated=False).order_by(
            'round')[1]

    def get_absolute_url(self):
        return f"/records/{self.season.league.pk}/{self.season.pk}/{self.pk}"

    def get_current_round(self) -> int | None:
        last_quiz = Quiz.objects.filter(event_id=self.pk).filter(isValidated=False).order_by('round').first()

        if last_quiz:
            return last_quiz.round
        else:
            return None

    def get_next_round(self) -> int | None:
        return self.get_current_round() + 1 if self.get_current_round() else None

    def get_event_view_data(self):
        with open('Records/queries/Event View.pgsql', 'r') as f:
            raw_query = f.read().replace('{event.id}', str(self.pk))

        teams = []

        with connection.cursor() as cursor:
            cursor.execute(raw_query)

            is_team_mate = False

            for row in cursor.fetchall():
                if not is_team_mate:
                    team = {
                        'code': row[0],
                        'name': row[1],
                        'score': (row[7] if row[7] is not None else 0) + (row[8] if row[8] is not None else 0),
                        'division': row[2],
                        'current_round': row[3],
                        'next_round': row[4],
                        'individuals': [
                            {
                                'name': row[6],
                                'score': (row[7] if row[7] is not None else 0) + (row[8] if row[8] is not None else 0),
                            },
                        ]
                    }
                    teams.append(team)
                else:
                    teams[-1]['individuals'].append({
                        'name': row[6],
                        'score': (row[7] if row[7] is not None else 0) + (row[8] if row[8] is not None else 0),
                    })

                    teams[-1]['score'] += (row[7] if row[7] is not None else 0) + (row[8] if row[8] is not None else 0)
                is_team_mate = not is_team_mate

        sorted_teams = sorted(teams, key=lambda t: (t['division'], t['score'], t['code']), reverse=True)

        # assign a rank to each team per division, and make each team tie that has the same score
        for division in set([t['division'] for t in sorted_teams]):
            division_teams = [t for t in sorted_teams if t['division'] == division]

            for i in range(len(division_teams)):
                if i > 0 and division_teams[i]['score'] == division_teams[i - 1]['score']:
                    division_teams[i]['rank'] = division_teams[i - 1]['rank']
                else:
                    division_teams[i]['rank'] = i + 1

        sorted_teams = sorted(teams, key=lambda t: (t['division'], t['rank'], t['code']))

        return sorted_teams

    def create_quiz(self, teams: list[Team], room: 'Room', round_number: Optional[int] = None,
                    quiz_type: str = 'tiebreaker'):

        if round_number is None:
            round_number = self.get_next_round()

        quiz = Quiz.objects.create(event=self, quiz_type=quiz_type,
                                   round=round_number, num_teams=len(teams),
                                   type=quiz_type, room=room)

        questions = AskedQuestion.objects.bulk_create([
            AskedQuestion(quiz=quiz, type=AskedQuestion.NORMAL, question_number=_ + 1)
            for _ in range(1, 16)])

        participants = QuizParticipants.objects.bulk_create([
            QuizParticipants(quiz=quiz, team=team) for team in teams])


class Room(models.Model):
    class Meta:
        unique_together = (('event', 'name'),)

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    quizmaster = models.ForeignKey(Individual, on_delete=models.CASCADE,
                                   related_name="quizmaster")  # , blank=True, null=True  ?
    scorekeeper = models.ForeignKey(Individual, on_delete=models.CASCADE,
                                    related_name="scorekeeper")  # , blank=True, null=True  ?

    def __str__(self) -> str:
        return self.name


class Quiz(models.Model):
    TIEBREAKER = 'tiebreaker'
    NORMAL = 'normal'

    QUIZ_TYPES = (
        (TIEBREAKER, 'Tiebreaker'),
        (NORMAL, 'Normal'),
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    round = models.IntegerField()
    isValidated = models.BooleanField(default=False)

    num_teams = models.IntegerField(default=3)

    type = models.CharField(max_length=10, choices=QUIZ_TYPES)

    allow_ties = models.BooleanField()

    ####
    # Included for backwards compatibility
    ####

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    # Quiz Progression

    # Event Progression
    # if Quiz.objects.filter(event=self.event, isValidated=False).exists():
    #     return

    # If there are ties...

    # breakpoints_within_division = [
    #     15,
    # ]

    # Get results
    # look for ties at breakpoints

    @property
    def quizmaster(self) -> Optional[Individual]:
        return self.room.quizmaster

    @property
    def scorekeeper(self) -> Optional[Individual]:
        return self.room.scorekeeper

    ####
    # /Included for backwards compatibility
    ####

    def __str__(self) -> str:
        return f"{self.room} - {self.round}"
        # return str(self.room) + str(self.round) + ' - ' + '  v  '.join(
        #     [str(team.try_short_name()) for team in self.get_teams()])

    def get_questions(self) -> QuerySet['AskedQuestion']:
        return AskedQuestion.objects.filter(quiz_id=self.pk)

    def get_teams(self):
        participants = QuizParticipants.objects.filter(quiz_id=self.pk).order_by('team__short_name')

        return [p.team for p in participants]

    # Results should be: {team: model: score: int, ...}
    def get_results(self) -> Dict[Team, Tuple[int, int]]:
        questions = self.get_questions()
        results = {}

        for team in self.get_teams():
            score = 40
            tiebreaker_score = 0

            for question in questions:
                if team.isMember(question.individual):
                    if question.type == AskedQuestion.NORMAL:
                        score += question.value
                    elif question.type == AskedQuestion.TIEBREAKER:
                        tiebreaker_score += question.value
                    elif question.type is None:
                        score += question.value

                    else:
                        raise NotImplementedError(f"Unknown question type: {question.type}")

                    # Handle nulls
                    if question.bonusValue:
                        score += question.bonusValue

            results[team] = (int(score), int(tiebreaker_score))

        return results

    def get_team_results(self, team: Team) -> int:
        results = self.get_results()

        return results[team][0]  # + results[team][1]

    def have_all_teams_validated(self):
        participants = QuizParticipants.objects.filter(quiz_id=self.pk)

        for participant in participants:
            if not participant.isValidated:
                return False

        return True

    def validated_by(self, individual: User):
        if individual == self.scorekeeper.user:
            self.isValidated = True
            self.save()
            return

        participants = QuizParticipants.objects.filter(quiz_id=self.pk)

        for participant in participants:
            if participant.team.isMember(individual):
                participant.isValidated = True
                participant.save()
                return
        else:
            raise Exception(f"{individual} is not the scorekeeper nor a member of any team in {self}")

    def add_tiebreaker(self):
        AskedQuestion.objects.create(quiz_id=self.pk, type=AskedQuestion.TIEBREAKER,
                                     question_number=AskedQuestion.objects.filter(quiz=self).count() + 1)

    def get_absolute_url(self):
        return f"/records/{self.event.season.league.pk}/{self.event.season.pk}/{self.event.pk}/{self.pk}"

    def add_team(self, team: Team):
        participants = QuizParticipants.objects.filter(quiz_id=self.pk)

        for participant in participants:
            if participant.team == team:
                raise ValueError(f"{team} is already a participant in {self}")

        QuizParticipants.objects.create(quiz_id=self.pk, team=team)

    def replace_team(self, old_team: Team, new_team: Team):
        participants = QuizParticipants.objects.filter(quiz_id=self.pk)

        for participant in participants:
            if participant.team == old_team:
                participant.delete()
                break
        else:
            raise ValueError(f"{new_team} is not a participant in {self}")

        self.add_team(new_team)

    def get_team_by_rank(self, rank: int) -> Team:
        results = self.get_results()

        if rank > len(results):
            raise ValueError(f"Rank {rank} is greater than the number of teams in {self}")

        return sorted(results.items(), key=lambda item: (item[1][0], item[1][1]))[rank - 1][0]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.advance_quizzes()

    def advance_quizzes(self):
        quiz_progression_objects = QuizProgression.objects.filter(quiz=self, isCompleted=False)

        if not quiz_progression_objects.exists():
            return

        for progression_object in quiz_progression_objects:
            try:
                next_quiz = Quiz.objects.get(event=self.event, room__name=progression_object.next_room,
                                             round=progression_object.next_round)
            except Quiz.DoesNotExist:
                raise ImproperlyConfigured(f"QuizProgression {progression_object} has no next quiz")

            QuizParticipants.objects.create(quiz=next_quiz, team=self.get_team_by_rank(progression_object.rank))

        division_progressions = QuizProgression.objects.filter(division__in=self.event.division_set, isCompleted=False)

        for division in self.event.division_set:
            quizzes = Quiz.objects.filter(isValidated=False, quizparticipants__team__in=division.teams)

            if quizzes.exists():
                continue

            # Check for meaningful ties
            progressions_no_ties = QuizProgression.objects.filter(division=division, isCompleted=False,
                                                                  allow_ties=False, type=QuizProgression.NORMAL)

            forced_unique_ranks = progressions_no_ties.values('rank')  # 8,15,23

            ranked_teams = division.get_ranked_teams()  # with ties

            ranks_in_ranked_teams = [team['rank'] for team in ranked_teams.values() if
                                     team['rank'] in forced_unique_ranks]

            for rank in forced_unique_ranks:
                if ranks_in_ranked_teams.count(rank) > 1:
                    # Quiz.objects.create(event=self.event, round=self.round + 1,
                    raise ValueError(f"Division {division} has a tie for rank {rank}")

            # Create QuizParticipants
            for index, team in enumerate(ranked_teams):
                rank = index + 1

                progression = QuizProgression.objects.get(division=division, isCompleted=False,
                                                          rank=rank, type=QuizProgression.NORMAL)

                QuizParticipants.objects.create(quiz=progression.next_quiz, team=team)

                if progression.next_division:
                    progression.next_division.teams.add(team)

                progression.isCompleted = True
                progression.save()

            ranks = []

            for team in ranked_teams:
                if ranks.count(team['rank']) == 0:
                    ranks.append(team['rank'])

                if len(ranks) == 3:
                    break


class QuizParticipants(models.Model):
    # class Meta:
    #     unique_together = ('quiz', 'team')

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    isValidated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quiz} - {self.team}"


class AskedQuestion(models.Model):
    CORRECT = 'correct'
    INCORRECT = 'incorrect'
    BONUS = 'bonus'

    NORMAL = 'normal'
    TIEBREAKER = 'tiebreaker'

    TYPE_CHOICES = (
        (NORMAL, 'Ok'),
        (TIEBREAKER, 'Tiebreaker'),
    )

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    individual = models.ForeignKey(Individual, on_delete=models.CASCADE, blank=True, null=True, default=None)

    question_number = models.IntegerField()
    ruling = models.CharField(max_length=100, blank=True, null=True)
    value = models.IntegerField(blank=True, null=True)

    type = models.CharField(max_length=100, choices=TYPE_CHOICES, blank=True, null=True)

    bonusValue = models.IntegerField(null=True, blank=True)
    bonusDescription = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.quiz} - {self.individual}: {self.ruling}"


class QuizProgression(models.Model):
    TIEBREAKER = 'tiebreaker'
    NORMAL = 'normal'

    PROGRESSION_TYPES = (
        (TIEBREAKER, 'Tiebreaker'),
        (NORMAL, 'Normal'),
    )

    type = models.CharField(max_length=100, blank=True, null=True, choices=PROGRESSION_TYPES)

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, blank=True, null=True)
    division = models.ForeignKey('Division', on_delete=models.CASCADE, blank=True, null=True)
    rank = models.IntegerField()
    next_quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='next_quiz')
    next_division = models.ForeignKey('Division', on_delete=models.CASCADE, blank=True, null=True,
                                      related_name='next_division')
    isCompleted = models.BooleanField(default=False)
    allow_ties = models.BooleanField(default=True)


class Division(models.Model):
    # class Meta:
        # unique_together = (('event', 'name'),)

    name = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    teams = models.ManyToManyField(Team)

    def get_division_view_data(self):
        with open('Records/queries/Division View.pgsql', 'r') as f:
            raw_query = f.read().replace('{event.id}', str(self.event.pk)).replace('{division.id}', str(self.pk))

        teams = []

        with connection.cursor() as cursor:
            cursor.execute(raw_query)

            is_team_mate = False

            for row in cursor.fetchall():
                if not is_team_mate:
                    team = {
                        'code': row[0],
                        'name': row[1],
                        'score': (row[7] if row[7] is not None else 0) + (row[8] if row[8] is not None else 0),
                        'current_round': row[3],
                        'next_round': row[4],
                        'individuals': [
                            {
                                'name': row[6],
                                'score': (row[7] if row[7] is not None else 0) + (row[8] if row[8] is not None else 0),
                            },
                        ]
                    }
                    teams.append(team)
                else:
                    teams[-1]['individuals'].append({
                        'name': row[6],
                        'score': (row[7] if row[7] is not None else 0) + (row[8] if row[8] is not None else 0),
                    })

                    teams[-1]['score'] += (row[7] if row[7] is not None else 0) + (row[8] if row[8] is not None else 0)
                is_team_mate = not is_team_mate

        sorted_teams = sorted(teams, key=lambda t: (t['score'], t['code']), reverse=True)

        for i in range(len(sorted_teams)):
            if i > 0 and sorted_teams[i]['score'] == sorted_teams[i - 1]['score']:
                sorted_teams[i]['rank'] = sorted_teams[i - 1]['rank']
            else:
                sorted_teams[i]['rank'] = i + 1

        sorted_teams = sorted(teams, key=lambda t: (t['rank'], t['code']))

        return sorted_teams

    def get_ranked_teams(self) -> List[Dict[str, Any]]:
        with open('Records/queries/Division View.pgsql', 'r') as f:
            raw_query = f.read().replace('{event.id}', str(self.event.pk)).replace('{division.id}', str(self.pk))

        with connection.cursor() as cursor:
            cursor.execute(raw_query)

            teams = []

            for row in cursor.fetchall():
                teams.append({
                    'code': row[0],
                    'name': row[1],
                    'score': (row[7] if row[7] is not None else 0) + (row[8] if row[8] is not None else 0),
                    'division': row[2],
                    'current_round': row[3],
                    'next_round': row[4],
                    'individuals': [
                        {
                            'name': row[6],
                            'score': (row[7] if row[7] is not None else 0) + (row[8] if row[8] is not None else 0),
                        },
                    ]
                })

        sorted_teams = sorted(teams, key=lambda item: item['score'], reverse=True)

        for i in range(len(sorted_teams)):
            if i > 0 and sorted_teams[i]['score'] == sorted_teams[i - 1]['score']:
                sorted_teams[i]['rank'] = sorted_teams[i - 1]['rank']
            else:
                sorted_teams[i]['rank'] = i + 1

        return sorted_teams
