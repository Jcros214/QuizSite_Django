import math

from django.db import models
from typing import List

# Create your models here.


# class Team(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
from Records.models import Team


class Bracket(models.Model):
    name = models.CharField(max_length=100)
    num_teams = models.IntegerField(default=16, choices=[(2 ** i, 2 ** i) for i in range(2, 7)])

    def __str__(self):
        return f"Bracket  - {self.name} ({self.num_teams} teams)"

    @staticmethod
    def create_with_matches(teams: List[Team], name: str = None):
        num_teams = len(teams)
        num_rounds = int(math.log(num_teams, 2))

        bracket = Bracket.objects.create(name=name if name else f"{num_teams} Team Bracket", num_teams=num_teams)

        # Start by creating the final match
        final_match = Match.objects.create(bracket=bracket, round=num_rounds)

        # Recursively create matches for the previous rounds
        bracket.create_matches(parent_match=final_match)

        seed_ctr = 1

        for match in Match.objects.filter(bracket=bracket, round=1):
            match.team1 = teams.pop(0)
            match.team1_seed = seed_ctr
            seed_ctr += 1
            match.team2 = teams.pop(0)
            match.team2_seed = seed_ctr
            seed_ctr += 1
            match.save()

        return bracket

    def create_matches(self, parent_match: 'Match' = None):
        # Base case: if parent is a leaf, return
        if parent_match.round == 1:
            return []

        # Recursive case: create two matches as children of parent, then make their children
        children = [
            Match.objects.create(bracket=self, round=parent_match.round - 1, parent_match=parent_match,
                                 is_upper_child=_) for _ in
            [True, False]
        ]
        for child in children:
            child.save()
            self.create_matches(parent_match=child)


class Match(models.Model):
    bracket = models.ForeignKey(Bracket, on_delete=models.CASCADE)
    round = models.IntegerField()
    parent_match = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None,
                                     related_name='child_match', blank=True)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team1", null=True, default=None)
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team2", null=True, default=None)
    team1_seed = models.IntegerField(default=None, null=True, blank=True)
    team2_seed = models.IntegerField(default=None, null=True, blank=True)
    team1_points = models.IntegerField(default=None, null=True, blank=True)
    team2_points = models.IntegerField(default=None, null=True, blank=True)

    is_upper_child = models.BooleanField(default=False)

    def __str__(self):
        try:
            if self.team1_points and self.team2_points:
                return f"{self.team1.name} ({self.team1_points}) vs {self.team2.name} ({self.team2_points})"
            return f"{self.team1.name} vs {self.team2.name}"
        except AttributeError:
            return f"Empty Match {self.pk}"

    def get_winner(self):
        if self.team1_points is None or self.team2_points is None:
            return None

        if self.team1_points > self.team2_points:
            return self.team1
        elif self.team2_points > self.team1_points:
            return self.team2

    def clear(self):
        self.team1_points = None
        self.team2_points = None
        self.team1 = None
        self.team2 = None
        self.save()

    def update_score(self, team: Team, score: int):
        need_refresh = False

        prv_winner = self.get_winner()

        if team == self.team1:
            self.team1_points = score
        elif team == self.team2:
            self.team2_points = score
        else:
            return f"Team {team} is not in match {self}"

        if prv_winner != (winner := self.get_winner()):
            need_refresh = True
            if prv_winner is None:
                if self.parent_match is not None:
                    self.parent_match.add_team(winner, self)
            else:
                match = self.parent_match
                match.replace_team(prv_winner, winner)
                match = match.parent_match
                while match:
                    match.clear()
                    match = match.parent_match

        self.save()

        if need_refresh:
            return "refresh"

    def add_team(self, team: Team, prv_match: 'Match' = None):
        if not prv_match.parent_match == self:
            return ValueError(f"Match {prv_match} is not a child of match {self}")

        if prv_match.is_upper_child:
            self.team1 = team
        else:
            self.team2 = team

        self.save()

    def replace_team(self, old_team: Team, new_team: Team):
        self.team1_points, self.team2_points = None, None

        if self.team1 == old_team:
            self.team1 = new_team
        elif self.team2 == old_team:
            self.team2 = new_team
        else:
            return ValueError(f"Team {old_team} is not in match {self}")

        self.save()

    def get_win_loss(self, team: Team):
        if self.get_winner() is None:
            return None
        return team == self.get_winner()

    def get_points(self, team: Team):
        if team == self.team1:
            return self.team1_points if self.team1_points is not None else ""
        elif team == self.team2:
            return self.team2_points if self.team2_points is not None else ""
        else:
            raise ValueError(f"Team {team} is not in match {self}")

    def team_in_match(self, team: Team) -> bool:
        return team == self.team1 or team == self.team2

    def get_rank(self, team: Team) -> Team:
        if self.team1 == team:
            return self.team1_seed
        elif self.team2 == team:
            return self.team2_seed
        else:
            raise ValueError(f"Team {team} is not in match {self}")
