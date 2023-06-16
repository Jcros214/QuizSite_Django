# Instead of picking matchups, then picking from those matchups, need to generate a correctly sized bracket...


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

NUM_ITERATIONS = 1

ROOMS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
NUM_ROUNDS = 12
DIVISIONS = ['R', 'G']
NUM_TEAMS = 36

DIV_ROUNDS = (len(ROOMS) * NUM_ROUNDS) / len(DIVISIONS)

from itertools import combinations
from random import choice, shuffle
import random
from typing import Tuple
# from dataclasses import dataclass

from concurrent.futures import ThreadPoolExecutor


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
        self.teams: list[Team]

    @staticmethod
    def generate_teams(divisions: list[str], teams: int) -> list['Division']:
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                   'U', 'V', 'W', 'X', 'Y', 'Z']

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

    # def find_unique_quizes(self, num_iterations=1, num_threads=8) -> list[Tuple[Team, Team, Team]]:
    #     unique_combo_sets = []
    #     team_combinations = list(combinations(self.teams, 3))
    #     unique_combinations = set()

    #     with ThreadPoolExecutor(max_workers=num_threads) as executor:
    #         futures = []

    #         for _ in range(num_iterations):
    #             random.shuffle(team_combinations)
    #             future = executor.submit(self._check_combinations, team_combinations[:])
    #             futures.append(future)

    #         for future in futures:
    #             valid_combinations = future.result()
    #             if len(valid_combinations) == DIV_ROUNDS:
    #                 unique_combo_sets.append(list(valid_combinations))
    #                 # print("Was valid")

    #             # unique_combinations.update(valid_combinations)

    #     unique_combo_sets = self.sort_by_fairness(unique_combo_sets)

    #     # print(f"{len(unique_combo_sets[0])} unique combos\n",
    #     #       ', '.join([f"{team.name}: {sum([unique_combo.count(team) for unique_combo in unique_combo_sets[0]])}"
    #     #                  for team in self.teams]))
    #     return unique_combo_sets[0]

    # def _check_combinations(self, team_combinations: list[Tuple[Team, Team, Team]]) -> list[Tuple[Team, Team, Team]]:
    #     valid_combinations = []

    #     for team_combo in team_combinations:
    #         is_valid = True

    #         for unique_combo in valid_combinations:
    #             common_teams = len([team for team in team_combo if team in unique_combo])

    #             if common_teams >= 2:
    #                 is_valid = False
    #                 break

    #         if is_valid:
    #             valid_combinations.append(team_combo)

    #     return valid_combinations

    # @staticmethod
    # def sort_by_fairness(unique_combo_sets: list[list[Tuple[Team, Team, Team]]]) -> list[list[Tuple[Team, Team, Team]]]:
    #     return sorted(unique_combo_sets, key=lambda combo_set: Division._get_fairness(combo_set))

    # @staticmethod
    # def _get_fairness(combo_set: list[Tuple[Team, Team, Team]]) -> float:
    #     set_of_teams = set()

    #     for combo in combo_set:
    #         set_of_teams.update(combo)

    #     matches_per_team = [sum([match.count(team) for match in combo_set]) for team in sorted(list(set_of_teams))]

    #     return max(matches_per_team) - min(matches_per_team)

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
    def __init__(self, rooms: list[str]):
        self.quizes = []
        self.quizes: list[Quiz]
        self.rooms = {}

        for room in rooms:
            self.rooms[room] = None

    # Throws an exception if the team is already in the round
    def add_quiz(self, quiz: Quiz, room: str):
        # Check that the teams are not in the round already
        for new_team in quiz.getTeams():
            for existing_team in self.getAllTeams():
                if new_team == existing_team:
                    raise Exception("Team already in round!")

        # Check that the room is not already taken
        if self.rooms[room] != None:
            raise Exception("Room already taken!")

        # Add the quiz to the round
        self.rooms[room] = quiz

    def getAllTeams(self):
        teams = []
        for quiz in self.quizes:
            teams += quiz.get_teams()
        return teams


class Bracket:
    def __init__(self, divisions: list[str] | list[Division], teams: int | None, rooms: list[str], rounds: int) -> None:
        if type(divisions) == list[Division]:
            self.divisions = divisions  # type: ignore
        else:
            self.divisions = Division.generate_teams(divisions, teams)  # type: ignore

        self.divisions: list[Division]

        self.num_rounds = rounds
        self.rooms = rooms

        self.rounds = []
        self.rounds: list[Round]

        self.generate_schedule_new()

    @property
    def teams(self) -> list[Team]:
        teams = []
        for division in self.divisions:
            teams += division.teams
        return teams

    def get_non_conflicting_quizzes(self, matchups: list[tuple[Team, Team, Team]], num_matchups: int) -> list[
        tuple[Team, Team, Team]]:
        # for _ in matchups, try to append to result, check if valid, if not, remove from result
        result = []

        while len(result) < num_matchups:
            shuffle(matchups)
            for new_matchup in matchups:
                result.append(new_matchup)
                result: list[tuple[Team, Team, Team]]

                for team in new_matchup:
                    for old_matchup in result[:-1]:
                        if team in old_matchup:
                            result.pop()
                            break
                    else:
                        continue
                    break

        return result

    # def generate(self):

    #     # if len(self.rooms) / len(self.divisions) % 1 != 0:
    #     #     raise Exception("Number of rooms must be divisible by the number of divisions")

    #     self.rounds = []
    #     self.rounds: list[Round]

    #     rooms_copy = self.rooms.copy()

    #     [self.rounds.append(Round(self.rooms)) for _ in range(self.num_rounds)]

    #     rounds_in_shared_rooms = []

    #     for division in self.divisions:
    #         num_rounds = (total_rounds := len(self.rooms) * self.num_rounds) / len(self.divisions) #42

    #         if num_rounds % 1 != 0:
    #             raise ValueError("Number of rounds must be divisible by the number of divisions!")
    #         else:
    #             num_rounds = int(num_rounds)

    #         # all_unique_matchups = division.find_unique_quizes(num_iterations=NUM_ITERATIONS)
    #         # selected_unique_matchups = [list(combo) for combo in combinations(all_unique_matchups, num_rounds)]
    #         # fairest_unique_matchups = Division.sort_by_fairness(selected_unique_matchups)[0]

    #         rooms = rooms_copy[:len(self.rooms) // len(self.divisions)]
    #         rooms_copy = rooms_copy[len(self.rooms) // len(self.divisions):]

    #         rounds_in_shared_room = len(self.rooms) % len(self.divisions)

    #         for round in self.rounds:
    #             matches = self.get_non_conflicting_quizzes(all_unique_matchups, len(rooms))
    #             for room in rooms:
    #                 round.add_quiz(
    #                     Quiz(list(matches.pop(0)))
    #                     , room
    #                 )

    def tabulate_rounds(self) -> str:
        output = []
        header = "|   |" + "|".join([f"{'Round ' + str(i + 1):^14}" for i in range(self.num_rounds)]) + "|"
        output.append(header)
        output.append("|---|" + "|".join(["-" * 14] * self.num_rounds) + "|")

        for room in self.rooms:
            rnd = [f"|{room:^3}|"]
            for round in self.rounds:
                quiz = round.rooms[room]
                if quiz:
                    rnd.append(f"{' v '.join([team.name for team in quiz.get_teams()]):^14}|")
                # else:
                #     output.append(f"| {room} |           |")
            output.append("".join(rnd))
        return "\n".join(output)

    def generate_schedule_new(self):
        self.schedule = {room: [] for room in self.rooms}

        for division in self.divisions:
            num_rooms = len(self.rooms) // len(self.divisions)
            rooms = self.rooms[:num_rooms]

            teams = division.teams

            shuffled_teams = teams.copy()

            schedule_copy = {room: [] for room in rooms}
            schedule_copy_copy = {room: [] for room in rooms}

            popped_teams = []
            popped_teams: list[Team]

            ctr = 0

            while len(list(schedule_copy.values())[-1]) < self.num_rounds:  # type: ignore
                shuffle(shuffled_teams)
                ctr += 1
                print(f'ctr: {ctr}') if ctr % 100 == 0 else None
                [popped_teams.append(shuffled_teams.pop()) for _ in range(3)]  # type: ignore
                self.add_match_to_next_slot(schedule_copy_copy, popped_teams)
                if self.test_schedule(schedule_copy_copy):
                    schedule_copy = self.deep_copy_dictionary(schedule_copy_copy)
                    popped_teams = []
                else:
                    schedule_copy_copy = self.deep_copy_dictionary(schedule_copy)
                    shuffled_teams += popped_teams
                    popped_teams = []

            for room, matches in schedule_copy.items():
                self.schedule[room] += matches

    def add_match_to_next_slot(self, schedule: dict, match: list[Team] | tuple[Team]):
        prv_len = 0
        for room, matches in schedule.items():
            if prv_len > len(matches):
                schedule[room].append(match)
                break
        else:
            first_key = list(schedule.keys())[0]
            schedule[first_key].append(match)

    def remove_match_from_prv_slot(self, schedule: dict, match: list[Team] | tuple[Team]):
        index_at_prv_len = [0]
        prv_len = 0
        for index, (room, matches) in enumerate(schedule.items()):
            if prv_len > len(matches):
                key_at_prv_len = list(schedule.keys())[index_at_prv_len[0]]
                schedule[key_at_prv_len].pop()
                break
            index_at_prv_len[0] = int(index)

        else:
            last_key = list(schedule.keys())[-1]
            schedule[last_key].remove(match)

    def test_schedule(self, schedule: dict):

        all_matches = []

        [[all_matches.append(match) for match in matches] for room, matches in schedule.items()]

        all_pairs = [tuple(combinations(match, 2)) for match in all_matches]

        if len(all_pairs) != len(set(all_pairs)):
            return False
        else:
            return True
        # for match in all_matches:
        #     for pair in combinations(match, 2):
        #         if pair in all_pairs:
        #             return False
        #         else:
        #             all_pairs.add(pair)

    def deep_copy_dictionary(self, dictionary: dict[str, list]) -> dict[str, list]:
        return {str(key): list(value) for key, value in dictionary.items()}


def calculate_team_statistics(bracket: Bracket):
    team_statistics = {}

    # Initialize the dictionary
    bracket.teams.sort()
    for team in bracket.teams:
        team_statistics[team.name] = {
            'total_quizzes': 0,
            'team_pairings': {},
        }

    for round in bracket.rounds:
        for room, quiz in round.rooms.items():
            if quiz:
                teams = quiz.get_teams()
                for team in teams:
                    team_statistics[team.name]['total_quizzes'] += 1

                    for paired_team in teams:
                        if paired_team != team:
                            if paired_team.name in team_statistics[team.name]['team_pairings']:
                                team_statistics[team.name]['team_pairings'][paired_team.name] += 1
                            else:
                                team_statistics[team.name]['team_pairings'][paired_team.name] = 1

    return team_statistics


if __name__ == "__main__":
    bracket = Bracket(DIVISIONS, NUM_TEAMS, ROOMS, NUM_ROUNDS)
    # print(bracket.tabulate_rounds())
    # print('\n\n\n\n\n\n')
    # print(calculate_team_statistics(bracket))
    print(bracket.schedule)
