from engine.game.player import Player
from engine.toolkit.combination import Combination


class GeneratorResponse:
    def __init__(self, players: list[Player], dealer: Player):
        self.players: list[Player] = players + [dealer]
        self.predictions: list[list[int]] = list()
        self.players_combinations: list[list[Combination]] = list()
        self.best_combinations: list[Combination] = list()

    def __repr__(self):
        return f"{self.players} {self.predictions}"
