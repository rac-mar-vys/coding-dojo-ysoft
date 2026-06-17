import unittest

from tennis_game import TennisGame


class TennisGameTest(unittest.TestCase):
    def test_happy_path_from_start_to_win(self) -> None:
        game = TennisGame("player1", "player2")

        expected_scores = [
            ("player1", "15-Love"),
            ("player2", "15-All"),
            ("player1", "30-15"),
            ("player2", "30-All"),
            ("player1", "40-30"),
            ("player2", "Deuce"),
            ("player1", "Advantage player1"),
            ("player1", "Win for player1"),
        ]

        self.assertEqual("Love-All", game.get_score())

        for winner, expected_score in expected_scores:
            game.won_point(winner)
            self.assertEqual(expected_score, game.get_score())

    def test_happy_path_player1_scores_all_points(self) -> None:
        game = TennisGame("player1", "player2")

        expected_scores = [
            ("player1", "15-Love"),
            ("player1", "30-Love"),
            ("player1", "40-Love"),
            ("player1", "Win for player1"),
        ]

        self.assertEqual("Love-All", game.get_score())

        for winner, expected_score in expected_scores:
            game.won_point(winner)
            self.assertEqual(expected_score, game.get_score())

    def test_negative_scores_are_not_allowed(self) -> None:
        game = TennisGame("player1", "player2")
        game._points["player1"] = -1

        with self.assertRaises(ValueError):
            game.get_score()

    def test_cannot_score_after_game_is_already_won(self) -> None:
        game = TennisGame("player1", "player2")

        for _ in range(4):
            game.won_point("player1")

        self.assertEqual("Win for player1", game.get_score())

        with self.assertRaises(ValueError):
            game.won_point("player1")

    def test_game_rejects_more_than_two_players(self) -> None:
        with self.assertRaises(TypeError):
            TennisGame("player1", "player2", "player3")

    def test_player_names_are_immutable_after_game_creation(self) -> None:
        game = TennisGame("player1", "player2")

        with self.assertRaises(AttributeError):
            game.player1_name = "renamed-player"


if __name__ == "__main__":
    unittest.main()
