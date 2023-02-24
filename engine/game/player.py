from engine.toolkit.card import Card


class Player:
    def __init__(self, name: str):
        self.name: str = name
        self.cards: list[Card] = list()

    def __repr__(self):
        return f"{self.name: <10} | {str(self.cards): <9}"

    def add(self, cards: list[Card]):
        self.cards.extend(cards)
