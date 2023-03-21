from django.db import models

class Orginization(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100)
    orginization = models.ForeignKey(Orginization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Individual(models.Model):
    name = models.CharField(max_length=100)
    birthday = models.DateField((""), auto_now=False, auto_now_add=False, default=None)

    def __str__(self):
        return self.name

class TeamMembership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    individual = models.ForeignKey(Individual, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Season(models.Model):
    name = models.CharField(max_length=100)
    # Should probably be changed to be first day of season...
    year = models.DateField((""), auto_now=False, auto_now_add=False)
    material = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.year.year}"


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
    # team: should teams be here or in another table (so it's not limited to 2 or 3)
    room = models.CharField(max_length=10)
    round = models.CharField(max_length=10)

    def __str__(self) -> str:
        return f"{self.event.name} - {self.room}{self.round}"

class QuizParticipants(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    team = models.ForeignKey(Individual, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class AskedQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_number = models.IntegerField()
    individual = models.ForeignKey(Individual, on_delete=models.CASCADE)
    ruleing = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.quiz} - {self.individual}: {self.ruleing}"
