from random import choice
from typing import Tuple, List


class RoundRobinScheduler:
    matches = set()
    named_matches = set()
    team_stats = {}
    rounds = set()
    full_teams = []

    def __init__(self, number_teams: int = 18, round_number: int = 4, matches_per_round: int = 5):
        self.teams = set(range(number_teams))
        self.round_number = round_number
        self.matches_per_round = matches_per_round

    @staticmethod
    def create_schedule(team_names: Tuple[str], number_teams: int = 18, round_number: int = 4,
                        matches_per_round: int = 5):
        scheduler = RoundRobinScheduler(number_teams, round_number, matches_per_round)
        scheduler.create_matches()
        scheduler.give_teams_names(team_names)
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
            self.team_stats[team_match_key]: list = [team]
            self.team_stats[team_count_key]: int = 0

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

            self.rounds.add(tuple(matches_for_round))


if __name__ == "__main__":
    teams = (
    "team1", "team2", "team3", "team4", "team5", "team6", "team7", "team8", "team9", "team10", "team11", "team12",
    "team13", "team14", "team15", "team16", "team17", "team18")
    print(RoundRobinScheduler.create_schedule(teams))





