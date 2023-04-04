from django.db import models

from django.contrib.auth.models import User


class Orginization(models.Model):
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
    orginization = models.ForeignKey(Orginization, on_delete=models.CASCADE)

class Individual(models.Model):
    name = models.CharField(max_length=100)
    birthday = models.DateField((""), auto_now=False, auto_now_add=False, default=None)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.name

class Season(models.Model):
    name = models.CharField(max_length=100)
    # Should probably be changed to be first day of season...
    year = models.DateField((""), auto_now=False, auto_now_add=False)
    material = models.CharField(max_length=100)
    league = models.ForeignKey(League, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.year.year}"
    
    def getTeams(self):
        return Team.objects.filter(season_id=self.pk)

class Team(models.Model):
    name = models.CharField(max_length=100)
    orginization = models.ForeignKey(Orginization, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def isMember(self, individual):
        return TeamMembership.objects.filter(team_id=self.pk, individual_id=individual.pk).exists()
    
    def url(self):
        return f"/records/{self.season.league.pk}/{self.season.pk}/team/{self.pk}"

class TeamMembership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    individual = models.ForeignKey(Individual, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.team.name} - {self.individual.name}"
class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField((""), auto_now=False, auto_now_add=False)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    location = models.ForeignKey(Orginization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Quiz(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    quizmaster = models.ForeignKey(Individual, on_delete=models.CASCADE)
    room = models.CharField(max_length=10)
    round = models.CharField(max_length=10)

    def __str__(self) -> str:
        return f"{self.event.name} - {self.room}{self.round}"
    
    def getQuestions(self):
        return AskedQuestion.objects.filter(quiz_id=self.pk)
    
    def getTeams(self):
        participants = QuizParticipants.objects.filter(quiz_id=self.pk)

        return [p.team for p in participants]
    
    # Results should be: {team: model: score: int, ...}
    def getResults(self):
        questions = self.getQuestions()
        results = {}

        for team in self.getTeams():
            score = 0

            for question in questions:
                if team.isMember(question.individual):
                    score += question.value
                    # Handle nulls
                    if question.bonusValue:
                        score += question.bonusValue

            results[team] = score
        
        return results

class QuizParticipants(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quiz} - {self.team}"


class AskedQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_number = models.IntegerField()
    individual = models.ForeignKey(Individual, on_delete=models.CASCADE)
    ruleing = models.CharField(max_length=100)
    value = models.IntegerField()
    bonusDescription = models.CharField(max_length=100, null=True, blank=True)
    bonusValue = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return f"{self.quiz} - {self.individual}: {self.ruleing}"
