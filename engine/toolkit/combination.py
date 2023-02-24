from __future__ import annotations

from engine.toolkit import constants
from engine.toolkit.card import Card


class Combination:
    def __init__(self, cards: tuple[Card, ...], name: str):
        self.cards: tuple[Card] = cards
        self.name: str = name

    def __repr__(self):
        return f"{self.name.capitalize()} [{self.power:.2f}] {list(self.cards)}"

    @property
    def power(self) -> float:
        full, add = constants.combination_powers[self.name], 0
        if self.name in ["high card", "pair", "three", "four"]:
            add = self.cards[0].rank
        elif self.name in ["two pair"]:
            add = self.cards[3].rank + self.cards[0].rank / 100
        elif self.name in ["straight", "straight flush"]:
            add = self.cards[1].rank
        elif self.name in ["flush"]:
            add = sum([card.rank / (100 ** index) for index, card in enumerate(reversed(self.cards))])
        elif self.name in ["full house"]:
            add = self.cards[4].rank + self.cards[0].rank / 100
        return full + add / 100
