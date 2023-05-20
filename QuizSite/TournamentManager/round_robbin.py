'''
Objectives:
    1. Each team should compete as many times as possible


    
Divisons:
    - ... should be ignored. 
    - They are basicly seperate tournaments (and unless they are skill based, are useless)
    - Exception: a number of rooms indivisible by the number of divisions

New Idea:
    - Find every possible bracket of specified size, sort by above
    - recursive decison tree? O(n!)...
    
    - get all combinations, as combos are used, remove all affected ones from round/whole/matches_num (ie, ones with the same teams in the same round won't work, but would work in a different round). If it fails, it is not possible as configured.
        - Try with byes? O(?) 

'''




from itertools import combinations
from random import choice, shuffle
from typing import Tuple
# from dataclasses import dataclass


class Division:
    def __init__(self, letter) -> None:
        self.letter = letter

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Division):
            return False
        
        return self.letter == __value.letter

class Team:
    def __init__(self, name, divison: Division):
        self.name = name
        self.divison = divison

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Team):
            return False
        
        return self.name == __value.name
    
    def __lt__(self, __value: object) -> bool:
        if not isinstance(__value, Team):
            return False

        return ((self.name) < (__value.name))

    def __gt__(self, __value: object) -> bool:
        if not isinstance(__value, Team):
            return False

        return ((self.name) > (__value.name))

    def __le__(self, __value: object) -> bool:
        if not isinstance(__value, Team):
            return False

        return ((self.name) <= (__value.name))

    def __ge__(self, __value: object) -> bool:
        if not isinstance(__value, Team):
            return False

        return ((self.name) >= (__value.name))

    def __hash__(self):
        return hash(self.name + self.divison.letter)


class Quiz:
    def __init__(self, teams: list[Team]):
        if len(teams) != 3:
            raise Exception("Quiz must have 3 teams")
        self.__teams = teams

    def getTeams(self) -> list[Team]:
        return self.__teams

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Quiz):
            return False
        
        return sorted(self.__teams) == sorted(__value.getTeams())

class Round:
    def __init__(self):
        self.quizes = []
        self.quizes: list[Quiz]
    
    # Throws an exception if the team is already in the round
    def add_quiz(self, quiz: Quiz):
        # Check that the teams are not in the round already
        for new_team in quiz.getTeams():
            for existing_team in self.getAllTeams():
                if new_team == existing_team:
                    raise Exception("Team already in round!")
        
        self.quizes.append(quiz)
    
    def getAllTeams(self):
        teams = []
        for quiz in self.quizes:
            teams += quiz.getTeams()
        return teams

class Bracket:
    def __init__(self, teams: list[Team], rounds: int, rooms: list[str]) -> None:
        self.teams = teams

        self.num_rounds = rounds
        self.rooms = rooms

        self.rounds = []
        self.rounds: list[Round]

        self.generate_attempts = 0

        while not self.generate():
            self.generate_attempts += 1
            if self.generate_attempts % 1000000 == 0:
                print(self.generate_attempts)


        # self.allUniqueMatchups = [division.generate_unique_matchups() for division in self.divisions]

    def getRandomTeam(self) -> Team:
        return choice(self.teams)

    def countTeamOccurances(self, team: Team) -> int:
        count = 0
        for round in self.rounds:
            for quiz in round.quizes:
                for quiz_team in quiz.getTeams():
                    if team == quiz_team:
                        count += 1
        return count

    def findMinTeamCount(self) -> Tuple[int, Team]: 
        teams = iter(self.teams)
        team = next(teams)

        min_count = self.countTeamOccurances(team)
        min_team = team

        for team in teams:
            if count := self.countTeamOccurances(team) < min_count:
                min_count = count
                min_team = team

        return min_count, min_team

    def doesTeamHaveMinCount(self, team: Team, minCount: int|None = None) -> bool:        
        if minCount is None:
            minCount = self.findMinTeamCount()[0]

        return self.countTeamOccurances(team) == minCount
    
    def getRandomTeamWithMinCount(self) -> Team:
        team = self.getRandomTeam()

        while not self.doesTeamHaveMinCount(team):
            team = self.getRandomTeam()
        
        return team

    '''
    Ensures that the given teams all have played the fewest number of times possible and have not played each other
    TODO: What if there is not a set of teams that can play together? Restart? Allow +/- 1 for min num?
    '''
    def canTeamPlayWith(self, teams) -> bool:
        minCount = self.findMinTeamCount()[0]

        if not all([self.doesTeamHaveMinCount(team, minCount) for team in teams]):
            return False
        
        for quiz in self.rounds[-1].quizes:
            for team in teams:
                if team in quiz.getTeams():
                    return False

        # check if teams is a subset of an existing quiz's teams
        for round in self.rounds[:-1]:
            for quiz in round.quizes:
                ctr = 0
                for team in teams:
                    if team in quiz.getTeams():
                       ctr += 1
                if ctr > 1:
                    return False 

        return True


    def generate(self):
        self.rounds = []
        self.rounds: list[Round]


        for round_num in range(self.num_rounds):
            self.rounds.append(Round())
            for room in self.rooms:
                teams = []
                teams.append(self.getRandomTeamWithMinCount())
                
                teamCopy = list(self.teams)
                shuffle(teamCopy)

                for team in teamCopy:
                    if self.canTeamPlayWith(teams + [team]):
                        teams += [team]
                        if len(teams) == 3:
                            self.rounds[round_num].add_quiz(Quiz(teams))
                            break
                else:
                    # raise Exception("Could not find a set of teams that can play together")
                    
                    f = False
                    return False




                # for division in self.divisions:
                #     round.add_quiz(division.generate_quiz())



            # for division in self.divisions:
            #     round.add_quiz(division.generate_quiz())
            # self.rounds.append(round)

    # def getCombos(self):
    #     return [[combo for combo in division.getCombos()] for division in self.divisions]


    



if __name__ == "__main__":
    brackets = []
    divisions = []
    teams = []
    for division in ['R', 'G']:
        for letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']:
            teams.append(division + letter)
        # divisions.append(Division(teams))

    brackets.append(Bracket(teams, 12, ["A", "B", "C", "D", "E", "F", "G"]))

    for bracket in brackets:
        print(bracket.rounds)