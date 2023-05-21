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

class Team:
    def __init__(self, name):
        self.name = name

    def __repr__(self) -> str:
        return f"<Team {self.name}>"

    # Equality operators

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
        return hash(self.name)

class Division:
    def __init__(self, letter) -> None:
        self.letter = letter
        self.teams = []

    @staticmethod
    def generate_teams(divisions: list[str], teams: int) -> list['Division']:
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

        teams_per_division = teams // len(divisions)

        if teams_per_division * len(divisions) != teams:
            raise Exception("Number of teams must be divisible by the number of divisions")

        divs = []
        divs: list[Division]

        for division in divisions:
            div = Division(division)
            
            for team in letters[:teams_per_division]:
                div.add_team(Team(division + team))
            
            divs.append(div)

        
        return divs
    
    def find_unique_quizes(self):
        unique_combo_sets = []
        team_combinations = list(combinations(self.teams, 3))
        unique_combinations = []

        shuffle(team_combinations)

        for team_combo in team_combinations:
            if len(unique_combinations) == 0:
                unique_combinations.append(team_combo)
                continue
            
            for unique_combo in unique_combinations:
                # Count the number of teams in common
                common_teams = len([team for team in team_combo if team in unique_combo])

                if common_teams >= 2:
                    break
            else:
                unique_combinations.append(team_combo)
                
        unique_combo_sets.append(unique_combinations)
        
        print(f"{len(unique_combinations)} unique combos\n", ', '.join([f"{team.name}: {sum([unique_combo.count(team) for unique_combo in unique_combinations])}" for team in division.teams])) # type: ignore


    def add_team(self, team: Team):
        self.teams.append(team)

    def conatins_team(self, team: Team) -> bool:
        return team in self.teams

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Division):
            return False
        
        return self.letter == __value.letter

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
    def __init__(self, divisions: list[str]|list[Division], teams: int|None, rooms: list[str], rounds: int) -> None:
        if type(divisions) == list[Division]:
            self.divisions = divisions # type: ignore
        else:
            self.divisions = Division.generate_teams(divisions, teams) # type: ignore

        self.divisions: list[Division]

        self.num_rounds = rounds
        self.rooms = rooms

        self.rounds = []
        self.rounds: list[Round]

        # self.generate_attempts = 0

        # while not self.generate():
        #     self.generate_attempts += 1
        #     if self.generate_attempts % 1000000 == 0:
        #         print(self.generate_attempts)


        # self.allUniqueMatchups = [division.generate_unique_matchups() for division in self.divisions]

    @property
    def teams(self) -> list[Team]:
        teams = []
        for division in self.divisions:
            teams += division.teams
        return teams

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
    def canTeamPlayWith(self, teams: list[Team]) -> bool:
        minCount = self.findMinTeamCount()[0]

        for division in self.divisions:
            if all([division.conatins_team(team) for team in teams]):
                break
        else:
            raise Exception("Teams must be in one division")
        

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

    def find_unique_matches(self):
        for division in self.divisions:
            division.find_unique_quizes()






if __name__ == "__main__":
    divisions = Division.generate_teams(['R', 'G'], 36)

    for division in divisions:
        division.find_unique_quizes()
