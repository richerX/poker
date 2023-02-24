import random

from engine.toolkit import constants
from engine.toolkit.card import Card


class Deck:
    def __init__(self):
        self.cards: list[Card] = []
        for rank in constants.ranks:
            for suite in constants.suites:
                self.cards.append(Card(rank, suite))

    def __repr__(self) -> str:
        return f"Deck = {self.cards}"

    def pick(self, count: int = 1) -> list[Card]:
        cards: list[Card] = list()
        for _ in range(count):
            card = random.choice(self.cards)
            self.cards.remove(card)
            cards.append(card)
        return cards

    def remove(self, card: Card):
        self.cards.remove(card)
