"""Tests for the tennis scoring kata.

Runs with the standard library test runner (no extra dependencies):

    python -m unittest test_tennis_game

It is also discoverable by pytest if that is installed:

    pytest
"""

import unittest

from tennis_game import TennisGame


def play(game: TennisGame, *winners: str) -> None:
    """Helper: record a sequence of point winners on ``game``."""
    for winner in winners:
        game.won_point(winner)


class BasicScoresTest(unittest.TestCase):
    def test_initial_score_is_love_all(self):
        self.assertEqual(TennisGame().get_score(), "Love-All")

    def test_single_point_for_player1(self):
        game = TennisGame()
        play(game, "player1")
        self.assertEqual(game.get_score(), "15-Love")

    def test_single_point_for_player2(self):
        game = TennisGame()
        play(game, "player2")
        self.assertEqual(game.get_score(), "Love-15")

    def test_running_score_30_15(self):
        game = TennisGame()
        play(game, "player1", "player2", "player1")
        self.assertEqual(game.get_score(), "30-15")

    def test_running_score_40_30(self):
        game = TennisGame()
        play(game, "player1", "player1", "player1", "player2", "player2")
        self.assertEqual(game.get_score(), "40-30")


class AllScoresTest(unittest.TestCase):
    def test_15_all(self):
        game = TennisGame()
        play(game, "player1", "player2")
        self.assertEqual(game.get_score(), "15-All")

    def test_30_all(self):
        game = TennisGame()
        play(game, "player1", "player2", "player1", "player2")
        self.assertEqual(game.get_score(), "30-All")

    def test_40_all_is_deuce_not_all(self):
        # At 3-3 both players have at least 3 points, so it is Deuce, not "40-All".
        game = TennisGame()
        play(game, "player1", "player2", "player1", "player2", "player1", "player2")
        self.assertEqual(game.get_score(), "Deuce")


class DeuceTest(unittest.TestCase):
    def test_deuce_at_three_all(self):
        game = TennisGame()
        play(game, "player1", "player2", "player1", "player2", "player1", "player2")
        self.assertEqual(game.get_score(), "Deuce")

    def test_deuce_returns_after_advantage(self):
        game = TennisGame()
        # 3-3 (Deuce), player1 advantage, player2 levels -> Deuce again.
        play(game, "player1", "player2", "player1", "player2", "player1", "player2")
        play(game, "player1")  # Advantage player1
        play(game, "player2")  # back to Deuce
        self.assertEqual(game.get_score(), "Deuce")


class AdvantageTest(unittest.TestCase):
    def test_advantage_player1(self):
        game = TennisGame()
        play(game, "player1", "player2", "player1", "player2", "player1", "player2")
        play(game, "player1")
        self.assertEqual(game.get_score(), "Advantage player1")

    def test_advantage_player2(self):
        game = TennisGame()
        play(game, "player1", "player2", "player1", "player2", "player1", "player2")
        play(game, "player2")
        self.assertEqual(game.get_score(), "Advantage player2")

    def test_advantage_uses_custom_names(self):
        game = TennisGame("Alice", "Bob")
        play(game, "Alice", "Bob", "Alice", "Bob", "Alice", "Bob")
        play(game, "Bob")
        self.assertEqual(game.get_score(), "Advantage Bob")


class WinTest(unittest.TestCase):
    def test_win_for_player1_to_love(self):
        game = TennisGame()
        play(game, "player1", "player1", "player1", "player1")
        self.assertEqual(game.get_score(), "Win for player1")

    def test_win_for_player2_to_30(self):
        game = TennisGame()
        play(game, "player2", "player1", "player2", "player1", "player2", "player2")
        self.assertEqual(game.get_score(), "Win for player2")

    def test_win_after_deuce_requires_two_point_lead(self):
        game = TennisGame()
        play(game, "player1", "player2", "player1", "player2", "player1", "player2")
        play(game, "player1")  # Advantage player1
        play(game, "player1")  # Win for player1
        self.assertEqual(game.get_score(), "Win for player1")

    def test_no_win_with_only_one_point_lead_at_four(self):
        # 4-3 is an advantage, not a win (lead of only one point).
        game = TennisGame()
        play(game, "player1", "player2", "player1", "player2", "player1", "player2", "player1")
        self.assertEqual(game.get_score(), "Advantage player1")

    def test_win_uses_custom_names(self):
        game = TennisGame("Alice", "Bob")
        play(game, "Bob", "Bob", "Bob", "Bob")
        self.assertEqual(game.get_score(), "Win for Bob")


class InterfaceTest(unittest.TestCase):
    def test_won_point_rejects_unknown_player(self):
        game = TennisGame("Alice", "Bob")
        with self.assertRaises(ValueError):
            game.won_point("Charlie")

    def test_duplicate_player_names_are_rejected(self):
        with self.assertRaises(ValueError):
            TennisGame("Sam", "Sam")


if __name__ == "__main__":
    unittest.main()
