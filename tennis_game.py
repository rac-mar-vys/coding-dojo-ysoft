"""Tennis scoring kata.

Implements the classic tennis game scoring rules behind a small interface:

    game = TennisGame("player1", "player2")
    game.won_point("player1")
    game.get_score()  # -> "15-Love"

Scoring rules:
    * Basic scores: points 0..3 map to "Love", "15", "30", "40".
    * All scores: equal scores below 3 points render as "Love-All" / "15-All" / "30-All".
    * Deuce: both players on at least 3 points and tied -> "Deuce".
    * Advantage: both on at least 3 points and one leads by exactly 1 -> "Advantage <name>".
    * Win: first to at least 4 points with a 2-point lead -> "Win for <name>".
"""

from __future__ import annotations

#: Names for the first four points won by a player.
POINT_NAMES = ("Love", "15", "30", "40")


class TennisGame:
    """Tracks the score of a single game of tennis between two players."""

    def __init__(self, player1_name: str = "player1", player2_name: str = "player2") -> None:
        if player1_name == player2_name:
            raise ValueError("The two players must have different names.")
        self.player1_name = player1_name
        self.player2_name = player2_name
        self._points: dict[str, int] = {player1_name: 0, player2_name: 0}

    def won_point(self, player_name: str) -> None:
        """Record that ``player_name`` won a point.

        Raises:
            ValueError: if ``player_name`` is not one of the two players.
        """
        if player_name not in self._points:
            raise ValueError(
                f"Unknown player {player_name!r}; expected "
                f"{self.player1_name!r} or {self.player2_name!r}."
            )
        self._points[player_name] += 1

    def get_score(self) -> str:
        """Return the current score as a human-readable string."""
        p1 = self._points[self.player1_name]
        p2 = self._points[self.player2_name]

        # Win: at least 4 points and a 2-point lead.
        if (p1 >= 4 or p2 >= 4) and abs(p1 - p2) >= 2:
            return f"Win for {self._leader(p1, p2)}"

        # Deuce / Advantage: both players have at least 3 points.
        if p1 >= 3 and p2 >= 3:
            if p1 == p2:
                return "Deuce"
            return f"Advantage {self._leader(p1, p2)}"

        # Equal scores below 3 points -> "<score>-All".
        if p1 == p2:
            return f"{POINT_NAMES[p1]}-All"

        # Otherwise, the two running scores side by side.
        return f"{POINT_NAMES[p1]}-{POINT_NAMES[p2]}"

    def _leader(self, p1: int, p2: int) -> str:
        """Return the name of the player currently in the lead."""
        return self.player1_name if p1 > p2 else self.player2_name


if __name__ == "__main__":
    # Tiny demo: play out a deuce -> advantage -> win sequence.
    game = TennisGame("Alice", "Bob")
    sequence = ["Alice", "Bob", "Alice", "Bob", "Alice", "Bob", "Alice", "Alice"]
    for winner in sequence:
        game.won_point(winner)
        print(f"{winner} scores -> {game.get_score()}")
