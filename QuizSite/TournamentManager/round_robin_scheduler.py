from random import choice
from typing import Tuple, List

LETTERS = [chr(_) for _ in range(65, 65 + 26)]

class ImpossibleSchedule(Exception):
    ...

class RoundRobinScheduler:
    matches: set[tuple[int, int, int]] = set()
    named_matches = set()
    team_stats = {}
    rounds = set()
    full_teams = []

    def __init__(self, number_teams: int = 18, round_number: int = 12, matches_per_round: int = 4):
        self.teams = set(range(number_teams))
        self.round_number = round_number
        self.matches_per_round = matches_per_round

    @staticmethod
    def create_schedule(team_names: list[str], number_teams: int = 18, round_number: int = 12,
                        matches_per_round: int = 4):
        scheduler = RoundRobinScheduler(number_teams, round_number, matches_per_round)
        scheduler.create_matches()
        scheduler.give_teams_names(team_names)
        if not scheduler.rounds:
            scheduler.create_rounds()
        return scheduler.rounds

    def get_matchable_team(self, teams : list[int] = []) -> int:
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

        # 1
        for team in teams:
            matchable_teams.remove(team)
        
        # 2
        for team in teams:
            for match in self.matches:
                if team in match:
                    [
                        matchable_teams.remove(rmteam) 
                        if rmteam in matchable_teams else '' 
                        for rmteam in match
                    ]
            
        ### RM ###
        from itertools import combinations

        have_played = set()

        for match in self.matches:
            have_played_len_start = len(have_played)
            
            for pair in combinations(match, 2):
                if pair in have_played:
                    raise ValueError("How did this happen??")
                else:
                    have_played.add(pair)

            

        # for team in self.teams:
        #     if len([match for match in self.matches if team in match])
        ### RM ###
                                    
        # 3 
        matchable_teams.sort(key = lambda team: len([match for match in self.matches if team in match]))

        try:
            return choice(matchable_teams)
        except:
            raise ImpossibleSchedule("No teams could be matched")

    def create_matches(self) -> None:
        """I'm using python's set type here so I can use the intersect shortcut"""
        self.matches = set()
        self.team_stats = {}

        for team in self.teams:
            team_match_key = f"team{team}"
            team_count_key = f"team{team}-count"
            self.team_stats[team_match_key] = [team]
            self.team_stats[team_count_key] = 0

        for team in self.teams:
            main_team_count_key = f"team{team}-count"
            while self.team_stats[main_team_count_key] < self.round_number:
                try:
                    team_match_1 = self.get_matchable_team([team])
                except ImpossibleSchedule:
                    break
                team1_match_key = f"team{team_match_1}"
                team_count_key = f"team{team_match_1}-count"
                self.team_stats[team1_match_key].append(team)
                self.team_stats[team_count_key] += 1

                team_match_2 = self.get_matchable_team([team_match_1, team])
                self.matches.add((team, team_match_1, team_match_2))

                team_match_key = f"team{team}"
                self.team_stats[team_match_key].extend([team_match_1, team_match_2])
                self.team_stats[main_team_count_key] += 1

                team_match_key = f"team{team_match_2}"
                team_count_key = f"team{team_match_2}-count"
                self.team_stats[team_match_key].extend([team_match_1, team])
                self.team_stats[team_count_key] += 1

                self.team_stats[team1_match_key].append(team_match_2)
            self.full_teams.append(team)

    def give_teams_names(self, names: list[str]) -> None:
        if len(names) < len(self.teams):
            raise ValueError("Not enough names")

        self.named_matches = set()
        for match in self.matches:
            named_match = []
            for team in match:
                named_match.append(names[team])
            self.named_matches.add(tuple(named_match))

    def create_rounds(self):
        matches = list(self.named_matches)
        for i in range(self.round_number):
            teams_in_round = set()
            matches_for_round = []

            for k in range(self.matches_per_round):
                match_to_add = choice(matches)
                while match_to_add in teams_in_round:
                    match_to_add = choice(matches)
                match_to_add = choice(matches)

                teams_in_round.add(match_to_add)
                matches.remove(match_to_add)
                matches_for_round.append(tuple(match_to_add))

                if k < self.matches_per_round - 1 and len(matches) == 0: 
                    # if we're not on the last match and there are no more matches to add 
                    # in other words, we've run out of matches to try
                    return False
            self.rounds.add(tuple(matches_for_round))



def tabulate_rounds(schedule, rooms_letters: list[str]) -> dict[str, list[str]]:
    num_rounds = len(schedule)
    
    rooms = {letter:[] for letter in rooms_letters}

    # convert from tuples to list
    sch = [list(list(sc) for sc in s) for s in schedule]

    for room in list(rooms.keys()):
        for rnd in sch:
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
            rnd.append(f"{' v '.join(quiz):^14}|")
        output.append("".join(rnd))

    print("\n".join(output))

    return rooms

def get_all_quizzes_from_schedule(schedule: dict[str, list[str]]) -> list[str]:
    quizzes = []
    for team in schedule:
        for quiz in schedule[team]:
            if quiz not in quizzes:
                quizzes.append(quiz)
            else:
                raise ValueError(f"Quiz {quiz} already in list")
    return quizzes

def find_fairness(teams: list[str], schedule: dict[str, list[str]]) -> dict[str, dict[str, int]]:
    fairness_dict = {}

    for team in teams:
        fairness_dict[team] = {team:0 for team in teams}

        for quiz in get_all_quizzes_from_schedule(schedule):
            if team in quiz:
                for quiz_team in quiz:
                    fairness_dict[team][quiz_team] += 1

    
    return fairness_dict


def main():
    teams = [f'R{_}' for _ in LETTERS[:18]]

    teamsets = [[f'{div}{_}' for _ in LETTERS[:18]] for div in ['R']]
    try:
        schedules = [RoundRobinScheduler.create_schedule(teams) for teams in teamsets]

        for schedule in schedules:

            dict_schedule = tabulate_rounds(schedule, LETTERS[:4])

            print(find_fairness(teams, dict_schedule), '\n\n')
    
        return True

    except ImpossibleSchedule as e:
        return
        


import multiprocessing

def run_main():
    # get cli arg 
    import sys
    if len(sys.argv) > 1:
        num_processes = int(sys.argv[1])
    else:
        raise ValueError('specify the number of processes to use')

    pool = multiprocessing.Pool(processes=num_processes)

    attempts = 0

    while True:
        results = [pool.apply_async(main) for _ in range(num_processes)]
        attempts += len(results)
        if attempts % 100000 == 0:
            print(f'still going... attempt {attempts}')
        for result in results:
            if result.get():
                pool.terminate()
                return

if __name__ == '__main__':
    run_main()