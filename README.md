# Tennis Scoring

A Python implementation of the classic tennis scoring kata.

## Interface

```python
from tennis_game import TennisGame

game = TennisGame("player1", "player2")  # names are optional
game.won_point("player1")
game.get_score()  # -> "15-Love"
```

## Tenis rules

## Scoring rules

| Situation | Output |
|-----------|--------|
| Points 0–3 | `Love`, `15`, `30`, `40` |
| Equal score below 3 points | `Love-All`, `15-All`, `30-All` |
| Both on ≥ 3 points and tied | `Deuce` |
| Both on ≥ 3 points, one leads by 1 | `Advantage player1` / `Advantage player2` |
| First to ≥ 4 points with a 2-point lead | `Win for player1` / `Win for player2` |

## Run

```bash
python tennis_game.py          # play a short demo game
python -m unittest test_tennis_game -v   # run the test suite
```

The tests use only the standard library (`unittest`), so no dependencies are
required. They are also discoverable by `pytest` if you have it installed.
