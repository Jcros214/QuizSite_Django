from random import choice
from typing import Tuple, List

LETTERS = [chr(_) for _ in range(65, 65 + 26)]

class ImpossibleSchedule(Exception):
    ...

class Team:
    def __init__(self, name) -> None:
        self.name = name
        self.count = 0

    def __repr__(self) -> str:
        return f'"{self.name}"'
    
    def __str__(self) -> str:
        return self.name

class RoundRobinScheduler:
    matches: set[tuple[int, int, int]] = set()
    named_matches = set()
    team_stats = {}
    rounds = set()
    full_teams = []

    def __init__(self, number_teams: int = 18, round_number: int = 12, matches_per_round: int = 3):
        self.teams = [Team(name) for name in LETTERS[:number_teams]]
        self.round_number = round_number
        self.matches_per_round = matches_per_round

    @staticmethod
    def create_schedule(team_names: list[str], number_teams: int = 18, round_number: int = 12,
                        matches_per_round: int = 4):
        scheduler = RoundRobinScheduler(number_teams, round_number, matches_per_round)
        scheduler.create_matches()
        return scheduler.rounds

    def have_played(self, team1: Team, team2: Team) -> int:
        for round in self.rounds:
            for quiz in round:
                if team1 in quiz and team2 in quiz:
                    return True
        return False

    def teams_have_played(self, team1: Team, team2: Team, team3: Team) -> int:
        
        return sum([int(self.have_played(*match)) for match in ((team1, team2), (team2, team3), (team1, team3))])

    # self.have_played(team1, team2) or self.have_played(team2, team3) or self.have_played(team1, team3)


    def get_triple_of_matchable_teams(self, round: list[list[Team]], excluded_teams: list[Team] = []) -> list[Team]:
        ''' A team is matchable if:
        1. It is not team_num
        2. It has not already competed against team_num
        3. It has the lowest number of matches (ie, has played the fewest of times) possible.
            - It may not be possible for team_num to match with a team that has played the fewest number of times
                - In this case, we will match with a team that has played the second fewest number of times and so on

        Create a list of teams, remove all teams who violate 1-2, then sort by 3

        Ideally, you'd also check if the team has already competed in this round, but that is not possible with the current structure.

        If no teams found, then the schedule is impossible. Need to start over (raise ImpossibleSchedule error)
        '''

        matchable_teams = list(self.teams)

        # # Remove teams already competeing in this round; these should not be considered
        for quiz in round:
            for team in quiz:
                matchable_teams.remove(team)

        # # Remove excluded teams
        # for team in excluded_teams:
        #     if team in matchable_teams:
        #         matchable_teams.remove(team)

        # # Group by the number of times they've played
        # team_dict = {team:0 for team in matchable_teams}

        # for match in self.matches:
        #     for team in match:
        #         if team in team_dict:
        #             team_dict[team] += 1

        # num_matches_per_team = {}

        # for team in team_dict:
        #     if team_dict[team] in num_matches_per_team:
        #         num_matches_per_team[team_dict[team]].append(team)
        #     else:
        #         num_matches_per_team[team_dict[team]] = [team]
                

        ### RM ###
        from itertools import combinations

        have_played = set()

        for match in self.matches:
            for pair in combinations(match, 2):
                if pair in have_played:
                    raise ValueError("How did this happen??")
                else:
                    have_played.add(pair)
        ### RM ###

        matchups = list(combinations(matchable_teams, 3))
        return list(sorted(matchups, key=lambda matchup: self.teams_have_played(*matchup))[0])



    def create_matches(self) -> None|bool:
        """I'm using python's set type here so I can use the intersect shortcut"""
        self.matches = set()
        self.team_stats = {}

        # Setup rounds as a 2d array
        self.rounds = [[[] for _ in  range(self.matches_per_round) ] for __ in  range(self.round_number)]


        for round_ind, round in enumerate(self.rounds):
            for quiz_ind, quiz in enumerate(round):
                self.rounds[round_ind][quiz_ind] = self.get_triple_of_matchable_teams(round)




def tabulate_rounds(schedule, rooms_letters: list[str]) -> dict[str, list[str]]:
    num_rounds = len(schedule)
    
    rooms = {letter:[] for letter in rooms_letters}

    # convert from tuples to list
    # sch = [list(list(sc) for sc in s) for s in schedule]

    for rnd in schedule:
        for room in list(rooms.keys()):
            rooms[room].append(rnd.pop(0))
        

        # rooms[].append(rnd.pop())


    # rooms = {letter:[schedule.pop() for _ in range(7)] for letter in LETTERS[:7]}

    output = []
    header = "|   |" + "|".join([f"{'Round ' + str(i+1):^14}" for i in range(num_rounds)]) + "|"
    output.append(header)
    output.append("|---|" + "|".join(["-"*14] * num_rounds) + "|")

    for room in rooms:
        rnd = [f"|{room:^3}|"]
        for quiz in rooms[room]:
            teams = [str(team) for team in quiz]
            rnd.append(f"{' v '.join(teams):^14}|")
        output.append("".join(rnd))

    print("\n".join(output))

    return rooms

def get_all_quizzes_from_schedule(schedule: dict[str, list[str]]) -> list[list[Team]]:
    quizzes = []
    for room in schedule:
        for quiz in schedule[room]:
            if quiz not in quizzes:
                quizzes.append(quiz)
            else:
                raise ValueError(f"Quiz {quiz} already in list")
    return quizzes

def find_fairness(teams: list[Team], schedule: dict[str, list[str]]) -> dict[str, dict[str, int]]:
    fairness_dict = {}

    for team in teams:
        fairness_dict[team] = {team:0 for team in teams}
        for quiz in get_all_quizzes_from_schedule(schedule):
            if team in quiz:
                for quiz_team in quiz:
                    fairness_dict[team][quiz_team] += 1

    
    return fairness_dict


def main():
    # teams = [f'R{_}' for _ in LETTERS[:18]]

    # teamsets = [[f'{div}{_}' for _ in LETTERS[:18]] for div in ['R']]
    try:
        scheduler = RoundRobinScheduler(matches_per_round=4)

        scheduler.teams = [Team(f'R{_}') for _ in LETTERS[:18]]

        scheduler.create_matches()

        schedule = scheduler.rounds
        
        dict_schedule = tabulate_rounds(schedule, LETTERS[:4])

        print(find_fairness(scheduler.teams, dict_schedule), '\n\n')

        return True

    except ImpossibleSchedule as e:
        print('tried...')
        return
        


# import multiprocessing

# def run_main():
#     # get cli arg 
#     from datetime import datetime
#     import sys
#     if len(sys.argv) > 1:
#         num_processes = int(sys.argv[1])
#     else:
#         raise ValueError('specify the number of processes to use')

#     pool = multiprocessing.Pool(processes=num_processes)

#     attempts = 0

#     while True:
#         results = [pool.apply_async(main) for _ in range(num_processes)]
#         attempts += len(results)
#         if attempts % 100000 == 0:
#             print(f'still going... attempt {attempts} {datetime.now()}')
#         for result in results:
#             if result.get():
#                 pool.terminate()
#                 return

# if __name__ == '__main__':
#     run_main()

if __name__ == '__main__':
    main()