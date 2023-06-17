from django.db import models
from Records.models import Quiz, Individual


# TODO: Is there a better way ot do this?

class ActiveScoreKeepers(models.Model):
    scorekeeper = models.ForeignKey(Individual, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
