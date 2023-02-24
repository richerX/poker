from __future__ import annotations

from engine.toolkit import constants


class Card:
    def __init__(self, rank: int, suit: str):
        self.rank: int = rank
        self.suit: str = suit

    def __eq__(self, other: Card):
        return self.rank == other.rank and self.suit == other.suit

    def __repr__(self):
        return f"{constants.ranks[self.rank]}{constants.suites[self.suit]}"
