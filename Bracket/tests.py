from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import Team, Match, Bracket


# Nothing really to test.
# class TeamModelTests(TestCase):
#     ...


# noinspection PyUnresolvedReferences
class MatchModelTests(TestCase):
    # Still needed:
    #   ensure team1 != team2
    #   untested methods:
    #       add_team
    #       replace_team

    @classmethod
    def setUpTestData(cls):
        cls.bracket = Bracket.objects.create(name="Bracket")
        cls.round = 1
        cls.team1 = Team.objects.create(name="Team 1")
        cls.team2 = Team.objects.create(name="Team 2")
        cls.team3 = Team.objects.create(name="Team 3")
        cls.parent_match = Match.objects.create(bracket=cls.bracket, round=(cls.round + 1))
        cls.empty_match = Match.objects.create(bracket=cls.bracket, round=cls.round)
        cls.match = Match.objects.create(bracket=cls.bracket, round=cls.round, team1=cls.team1, team2=cls.team2,
                                         parent_match=cls.parent_match)

    # Create strs
    def test_str_empty(self):
        self.assertEqual(str(self.empty_match), f"Empty Match {self.empty_match.pk}")

    def test_str_team1(self):
        self.empty_match.team1 = self.team1
        self.assertEqual(str(self.empty_match), f"Empty Match {self.empty_match.pk}")

    def test_str_team2(self):
        self.empty_match.team2 = self.team2
        self.assertEqual(str(self.empty_match), f"Empty Match {self.empty_match.pk}")

    def test_str_no_points(self):
        self.assertEqual(str(self.match), f"Team 1 vs Team 2")

    def test_str_points(self):
        self.match.team1_points = 10
        self.match.team2_points = 5

        self.assertEqual(str(self.match), f"Team 1 (10) vs Team 2 (5)")

    # get_winner
    def test_get_winner_none(self):
        self.assertIsNone(self.match.get_winner())

    def test_get_winner_team1_points_only(self):
        self.match.team1_points = 10
        self.assertIsNone(self.match.get_winner())

    def test_get_winner_team2_points_only(self):
        self.match.team2_points = 10
        self.assertIsNone(self.match.get_winner())

    def test_get_winner_team1(self):
        self.match.team1_points = 10
        self.match.team2_points = 5
        self.assertEqual(self.match.get_winner(), self.team1)

    def test_get_winner_team2(self):
        self.match.team1_points = 5
        self.match.team2_points = 10
        self.assertEqual(self.match.get_winner(), self.team2)

    def test_get_winner_tie(self):
        self.match.team1_points = 10
        self.match.team2_points = 10
        self.assertIsNone(self.match.get_winner())

    # clear
    def test_clear(self):
        self.match.team1_points = 10
        self.match.team2_points = 5

        self.match.clear()

        self.assertIsNone(self.match.team1)
        self.assertIsNone(self.match.team2)
        self.assertIsNone(self.match.team1_points)
        self.assertIsNone(self.match.team2_points)

        self.assertEqual(self.match.bracket, self.bracket)
        self.assertEqual(self.match.round, self.round)
        self.assertEqual(self.match.parent_match, self.parent_match)

    # update score

    #  note that unless otherwise specified, default values are None
    #  values on this side are before the method call      ->      and values on this side are after the method call
    #  if  -> is not used, all values before the method call are default, and the values given are after the method call

    #   doesn't need refresh
    #       winner is None -> winner is None
    #  1        given team not in match
    #  2        (team1_points is not None) and (team2_points is None)
    #  3        (team2_points is not None) and (team1_points is None)
    #           team1_points == team2_points
    #       winner is not None -> winner == prv_winner
    #  4        team1_points > team2_points -> team1_points > team2_points
    #  5        team1_points < team2_points -> team1_points < team2_points
    #   needs refresh
    #       prv_winner is not None -> winner is None
    #  6        team1_points > team2_points -> team1_points == team2_points
    #  7        team1_points < team2_points -> team1_points == team2_points
    #       prv_winner is None -> winner is not None
    #  8        team1_points > team2_points
    #  9        team1_points < team2_points
    #       prv_winner is not None -> (winner is not None) and (prv_winner != winner)
    #  10       team1_points > team2_points -> team1_points < team2_points
    #  11       team1_points < team2_points -> team1_points > team2_points

    def test_update_score_team_not_in_match(self):
        """1"""
        result = self.match.update_score(self.team3, 10)

        self.assertIsNone(self.match.team1_points)
        self.assertIsNone(self.match.team2_points)
        self.assertEqual(result, f"Team {self.team3} is not in match {self.match}")

        self.assertFalse(self.match.parent_match.team_in_match(self.team1))
        self.assertFalse(self.match.parent_match.team_in_match(self.team2))

    def test_update_score_team1_points_only(self):
        """2"""
        result = self.match.update_score(self.team1, 10)

        self.assertEqual(self.match.team1_points, 10)
        self.assertIsNone(self.match.team2_points)
        self.assertIsNone(result)

        self.assertFalse(self.match.parent_match.team_in_match(self.team1))
        self.assertFalse(self.match.parent_match.team_in_match(self.team2))

    def test_update_score_team2_points_only(self):
        """3"""
        result = self.match.update_score(self.team2, 10)

        self.assertIsNone(self.match.team1_points)
        self.assertEqual(self.match.team2_points, 10)
        self.assertIsNone(result)

        self.assertFalse(self.match.parent_match.team_in_match(self.team1))
        self.assertFalse(self.match.parent_match.team_in_match(self.team2))

    def test_update_score_team1_wins_result_unchanged(self):
        """4"""
        self.match.update_score(self.team1, 10)
        self.match.update_score(self.team2, 5)

        self.assertTrue(self.match.parent_match.team_in_match(self.team1))
        self.assertFalse(self.match.parent_match.team_in_match(self.team2))

        result = self.match.update_score(self.team1, 15)

        # DRY
        # self.assertEqual(self.match.team1_points, 15)
        # self.assertEqual(self.match.team2_points, 5)
        self.assertIsNone(result)

        self.assertTrue(self.match.parent_match.team_in_match(self.team1))
        self.assertFalse(self.match.parent_match.team_in_match(self.team2))

    def test_update_score_team2_wins_result_unchanged(self):
        """5"""
        self.match.update_score(self.team1, 5)
        self.match.update_score(self.team2, 10)

        self.assertTrue(self.match.parent_match.team_in_match(self.team2))
        self.assertFalse(self.match.parent_match.team_in_match(self.team1))

        result = self.match.update_score(self.team2, 15)

        # DRY
        # self.assertEqual(self.match.team1_points, 5)
        # self.assertEqual(self.match.team2_points, 15)
        self.assertIsNone(result)

        self.assertTrue(self.match.parent_match.team_in_match(self.team2))
        self.assertFalse(self.match.parent_match.team_in_match(self.team1))

    def test_update_score_team1_won_but_now_tied(self):
        """6"""
        self.match.update_score(self.team1, 10)
        self.match.update_score(self.team2, 5)

        # DRY
        # self.assertTrue(self.match.parent_match.team_in_match(self.team1))
        # self.assertFalse(self.match.parent_match.team_in_match(self.team2))

        result = self.match.update_score(self.team1, 5)

        # DRY
        # self.assertEqual(self.match.team1_points, 5)
        # self.assertEqual(self.match.team2_points, 5)
        self.assertEqual(result, "refresh")

        self.assertFalse(self.match.parent_match.team_in_match(self.team1))
        self.assertFalse(self.match.parent_match.team_in_match(self.team2))

    def test_update_score_team2_won_but_now_tied(self):
        """7"""
        self.match.update_score(self.team1, 5)
        self.match.update_score(self.team2, 10)

        # DRY
        # self.assertTrue(self.match.parent_match.team_in_match(self.team2))
        # self.assertFalse(self.match.parent_match.team_in_match(self.team2))

        result = self.match.update_score(self.team2, 5)

        # DRY
        # self.assertEqual(self.match.team1_points, 5)
        # self.assertEqual(self.match.team2_points, 5)
        self.assertEqual(result, "refresh")

        self.assertFalse(self.match.parent_match.team_in_match(self.team1))
        self.assertFalse(self.match.parent_match.team_in_match(self.team2))

    def test_update_score_both_team1_wins(self):
        """8"""
        result1 = self.match.update_score(self.team1, 10)
        result2 = self.match.update_score(self.team2, 5)

        self.assertEqual(self.match.team1_points, 10)
        self.assertEqual(self.match.team2_points, 5)
        self.assertIsNone(result1)
        self.assertEqual(result2, "refresh")

        self.assertTrue(self.match.parent_match.team_in_match(self.team1))
        self.assertFalse(self.match.parent_match.team_in_match(self.team2))

    def test_update_score_both_team2_wins(self):
        """9"""
        result1 = self.match.update_score(self.team1, 5)
        result2 = self.match.update_score(self.team2, 10)

        self.assertEqual(self.match.team1_points, 5)
        self.assertEqual(self.match.team2_points, 10)
        self.assertIsNone(result1)
        self.assertEqual(result2, "refresh")

        self.assertFalse(self.match.parent_match.team_in_match(self.team1))
        self.assertTrue(self.match.parent_match.team_in_match(self.team2))

    def test_update_score_team1_won_but_now_team2_wins(self):
        """10"""
        self.match.update_score(self.team1, 10)
        self.match.update_score(self.team2, 5)

        result = self.match.update_score(self.team2, 15)

        self.assertEqual(self.match.team1_points, 10)
        self.assertEqual(self.match.team2_points, 15)
        self.assertEqual(result, "refresh")

        self.assertFalse(self.match.parent_match.team_in_match(self.team1))
        self.assertTrue(self.match.parent_match.team_in_match(self.team2))

    def test_update_score_team2_won_but_now_team1_wins(self):
        """11"""
        self.match.update_score(self.team1, 5)
        self.match.update_score(self.team2, 10)

        result = self.match.update_score(self.team1, 15)

        self.assertEqual(self.match.team1_points, 15)
        self.assertEqual(self.match.team2_points, 10)
        self.assertEqual(result, "refresh")

        self.assertTrue(self.match.parent_match.team_in_match(self.team1))
        self.assertFalse(self.match.parent_match.team_in_match(self.team2))


class BracketModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.bracket = Bracket.objects.create(name="Bracket", num_teams=4)

    def test_try_invalid_number_of_teams(self):
        with self.assertRaises(ValidationError):
            Bracket.objects.create(name="Bracket", num_teams=3).full_clean()

    # create matches
    def test_every_match_has_2_children(self):
        """Exclude matches in round 1 that should have no children"""
        for num_teams in [4, 8, 16, 32, 64]:
            teams = [Team.objects.create(name=f"Team {i}") for i in range(1, num_teams + 1)]

            bracket = Bracket.create_with_matches(teams, "Bracket")

            for match in Match.objects.filter(bracket=bracket).exclude(round=1):
                self.assertEqual(match.child_match.count(), 2,
                                 f"Match {match} has {match.child_match.count()} children")

    def test_right_num_matches_for_num_teams(self):
        for num_teams in [4, 8, 16, 32, 64]:
            teams = [Team.objects.create(name=f"Team {i}") for i in range(1, num_teams + 1)]

            bracket = Bracket.create_with_matches(teams, "Bracket")

            self.assertEqual(Match.objects.filter(bracket=bracket).count(), num_teams - 1)
