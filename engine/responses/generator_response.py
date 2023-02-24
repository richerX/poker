from engine.game.player import Player


class GeneratorResponse:
    def __init__(self, players: list[Player], dealer: Player):
        self.players: list[Player] = players
        self.dealer: Player = dealer
        self.predictions: list[list[int]] = list()

    def __repr__(self):
        return f"{self.players} {self.dealer} {self.predictions}"
