from dataclasses import dataclass
from typing import Union

from engine.game.player import Player
from engine.toolkit.combination import Combination
from engine.toolkit.card import Card
from engine.toolkit.constants import *


@dataclass
class PlayerContext:
    player: Player
    prediction: int
    combination: Combination
    files: list[str]


@dataclass
class StageContext:
    stage: int
    players_context: list[PlayerContext]
    dealer_context: list[PlayerContext]


class GeneratorResponse:
    def __init__(self, players: list[Player], dealer: Player):
        self.players: list[Player] = players
        self.dealer: Player = dealer
        self.predictions: list[list[int]] = list()
        self.players_combinations: list[list[Combination]] = list()
        self.best_combinations: list[Combination] = list()

    def __repr__(self) -> str:
        return f"{self.players} {self.predictions}"

    def get_context(self) -> list[StageContext]:
        stages: list[StageContext] = list()
        for stage in range(len(tours)):
            # Players context
            best_combination = self.best_combinations[stage]
            players_context: list[PlayerContext] = list()
            for player, prediction, combination in zip(self.players, self.predictions[stage], self.players_combinations[stage]):
                players_context.append(PlayerContext(player, prediction, combination, [self.get_card_file(card, best_combination) for card in player.cards]))

            # Dealer context
            dealer_context: list[PlayerContext] = list()
            shown_cards: int = sum(tours[:stage + 1])
            dealer_predictions: int = self.predictions[stage][-1]
            dealer_combination: Union[Combination, None] = None
            dealer_cards: list[Union[Card, None]] = self.dealer.cards[:shown_cards] + [None] * (sum(tours) - shown_cards)
            dealer_context.append(PlayerContext(self.dealer, dealer_predictions, dealer_combination, [self.get_card_file(card, best_combination) for card in dealer_cards]))

            # Stages
            stages.append(StageContext(stage, players_context, dealer_context))
        return stages

    @staticmethod
    def get_card_file(card, combination):
        if card is None:
            return "jokers.png"
        return f"{card.rank}-{card.suit}{'-frame' if card in combination.cards else ''}.png"
