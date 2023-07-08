from typing import Optional, Dict, Tuple

from django.core.exceptions import ImproperlyConfigured
from django.db import models

from django.contrib.auth.models import User
from django.db.models import QuerySet
import django.utils.timezone
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
    division = models.CharField(max_length=2, blank=True, null=True)

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

    def get_team_rank_in_division(self, team: Team):
        teams = sorted(self.season.get_teams(), key=lambda t: self.get_team_score(t), reverse=True)

        rank = 1

        for ranked_team in teams:
            if team == ranked_team:
                return rank
            elif ranked_team.division == team.division:
                rank += 1
        else:
            raise ValueError(f"Team {team} is not in this event")

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
        raw_query = f'''
    select
    t.short_name,
    t.name as teamname,
    t.division as division,
    cr.id as currentround,
    nr.id as nextround,
    i.id as individualid,
    i.name as individualname,
    sum(coalesce(aq.value, 0)) as points,
    cr2.attendancepoints as attendancepoints
from "Records_team" t
left join "Records_teammembership" tm on tm.team_id = t.id
left join "Records_individual" i on tm.individual_id = i.id
left join "Records_quizparticipants" qp on qp.team_id = t.id
left join "Records_quiz" rq on qp.quiz_id = rq.id
left join "Records_event" e on rq.event_id = e.id
left join "Records_askedquestion" aq on aq.individual_id = i.id and aq.quiz_id = rq.id
left join (
    SELECT qp.team_id, rqc.id
    from "Records_quizparticipants" qp
    left join "Records_quiz" rqc on qp.quiz_id = rqc.id
    where cast(rqc.round as int) = (select min(cast(rq1.round as int)) from "Records_quiz" rq1 where rq1."isValidated" = false)
) as cr on cr.team_id = t.id
left join (
    SELECT qp.team_id, rqn.id
    from "Records_quizparticipants" qp
    left join "Records_quiz" rqn on qp.quiz_id = rqn.id
    where cast(rqn.round as int) = ((select min(cast(rq2.round as int)) from "Records_quiz" rq2 where rq2."isValidated" = false) + 1)
) as nr on nr.team_id = t.id
left join (
    SELECT qp.team_id, count(qp.team_id)*20 as attendancepoints
    from "Records_quizparticipants" qp
    left join "Records_quiz" rqc2 on qp.quiz_id = rqc2.id
    where cast(rqc2.round as int) <= (select min(cast(rq3.round as int)) from "Records_quiz" rq3 where rq3."isValidated" = false)
    group by qp.team_id
) as cr2 on cr2.team_id = t.id
where e.id = {self.pk}
group by
    t.short_name,
    t.name,
    t.division,
    cr.id,
    nr.id,
    i.id,
    i.name,
    cr2.attendancepoints
order by t.short_name, i.id

        
        '''

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

    ####
    # Included for backwards compatibility
    ####

    def save(self, *args, **kwargs):
        # Quiz Progression

        # Event Progression
        if Quiz.objects.filter(event=self.event, isValidated=False).exists():
            return

        # If there are ties...

        breakpoints_within_division = [
            15,

        ]

        # Get results
        # look for ties at breakpoints

        super().save(*args, **kwargs)

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
        return str(self.room) + str(self.round) + ' - ' + '  v  '.join(
            [str(team.try_short_name()) for team in self.get_teams()])

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
                    else:
                        raise NotImplementedError("Unknown question type")

                    # Handle nulls
                    if question.bonusValue:
                        score += question.bonusValue

            results[team] = (score, tiebreaker_score)

        return results

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

    def advance_quizzes(self):
        progression_objects = QuizProgression.objects.filter(event=self.event, room=self.room.name, round=self.round)

        if not progression_objects.exists():
            return

        for progression_object in progression_objects:
            # Get next quiz
            try:
                next_quiz = Quiz.objects.get(event=self.event, room__name=progression_object.next_room,
                                             round=progression_object.next_round)
            except Quiz.DoesNotExist:
                raise ImproperlyConfigured(f"QuizProgression {progression_object} has no next quiz")

            QuizParticipants.objects.create(quiz=next_quiz, team=self.get_team_by_rank(progression_object.rank))


class QuizParticipants(models.Model):
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

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    division = models.CharField(max_length=30)
    rank = models.IntegerField()
    next_room = models.CharField(max_length=10)
    next_round = models.IntegerField()
