from random import choice
from typing import Tuple, List

LETTERS = [chr(_) for _ in range(65, 65 + 26)]

class RoundRobinScheduler:
    matches = set()
    named_matches = set()
    team_stats = {}
    rounds = set()
    full_teams = []

    def __init__(self, number_teams: int = 18, round_number: int = 12, matches_per_round: int = 4):
        self.teams = set(range(number_teams))
        self.round_number = round_number
        self.matches_per_round = matches_per_round

    @staticmethod
    def create_schedule(team_names: Tuple[str], number_teams: int = 18, round_number: int = 12,
                        matches_per_round: int = 4):
        scheduler = RoundRobinScheduler(number_teams, round_number, matches_per_round)
        scheduler.create_matches()
        scheduler.give_teams_names(team_names)
        if not scheduler.rounds:
            scheduler.create_rounds()
        return scheduler.rounds

    def get_matchable_team(self, team_num: int) -> int:
        team_match_key = f"team{team_num}"
        remaining_teams = self.teams.difference(self.full_teams)
        matchable_teams = list(remaining_teams ^ set(self.team_stats[team_match_key]))  # XOR operator... get everything that is not in common between the two sets
        return choice(matchable_teams)

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
                team_match_1 = self.get_matchable_team(team)
                team1_match_key = f"team{team_match_1}"
                team_count_key = f"team{team_match_1}-count"
                self.team_stats[team1_match_key].append(team)
                self.team_stats[team_count_key] += 1

                team_match_2 = self.get_matchable_team(team_match_1)
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

    def give_teams_names(self, names: Tuple[str]) -> None:
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

    teamsets = [[f'{div}{_}' for _ in LETTERS[:18]] for div in ['R', 'G']]
    try:
        schedules = [RoundRobinScheduler.create_schedule(teams) for teams in teamsets]

        for schedule in schedules:

            dict_schedule = tabulate_rounds(schedule, LETTERS[:4])

            print(find_fairness(teams, dict_schedule), '\n\n')
    
        return True

    except Exception as e:
        print(e)
        





if __name__ == "__main__":
    while not main():
        main()