from django.db import models

from django.contrib.auth.models import User
from django.db.models import QuerySet
import django.utils.timezone
from django.utils.functional import SimpleLazyObject


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
    name = models.CharField(max_length=100)
    birthday = models.DateField("", auto_now=False, auto_now_add=False, default=None, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

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


class Team(models.Model):
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    short_name = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

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

    def url(self):
        return f"/records/{self.season.league.pk}/{self.season.pk}/team/{self.pk}"


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

    def __str__(self):
        return f"{self.season} - {self.date.month}"

    def date_is_today(self):
        return self.date == django.utils.timezone.datetime.date.today()


class Quiz(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    quizmaster = models.ForeignKey(Individual, on_delete=models.CASCADE, related_name="quizmaster")
    scorekeeper = models.ForeignKey(Individual, on_delete=models.CASCADE, related_name="scorekeeper")
    room = models.CharField(max_length=10)
    round = models.CharField(max_length=10)
    isValidated = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.room}{self.round} - " + ' v '.join([str(team.try_short_name()) for team in self.get_teams()])

    def get_questions(self) -> QuerySet['AskedQuestion']:
        return AskedQuestion.objects.filter(quiz_id=self.pk)

    def get_teams(self):
        participants = QuizParticipants.objects.filter(quiz_id=self.pk)

        return [p.team for p in participants]

    # Results should be: {team: model: score: int, ...}
    def get_results(self):
        questions = self.get_questions()
        results = {}

        for team in self.get_teams():
            score = 0

            for question in questions:
                if team.isMember(question.individual):
                    score += question.value
                    # Handle nulls
                    if question.bonusValue:
                        score += question.bonusValue

            results[team] = score

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


class QuizParticipants(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    isValidated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quiz} - {self.team}"


class AskedQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    individual = models.ForeignKey(Individual, on_delete=models.CASCADE, blank=True, null=True, default='')

    question_number = models.IntegerField()
    ruling = models.CharField(max_length=100, blank=True, null=True)
    value = models.IntegerField(blank=True, null=True)

    bonusValue = models.IntegerField(null=True, blank=True)
    bonusDescription = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.quiz} - {self.individual}: {self.ruling}"
