from typing import Tuple

from engine.game.deck import Deck
from engine.game.player import Player
from engine.toolkit import constants
from engine.toolkit.combination import Combination
from engine.toolkit.collection import Collection
from engine.toolkit.predictor import Predictor
from engine.responses.generator import GeneratorResponse


class Game:
    def __init__(self, players: int = 2, display: bool = False):
        self.deck: Deck = Deck()
        self.dealer: Player = Player("Dealer")
        self.players: list[Player] = [Player(f"Player #{i + 1}") for i in range(players)]
        self.display = display

    def play(self) -> GeneratorResponse:
        for player in self.players:
            player.add(self.deck.pick(constants.start_cards))

        response = GeneratorResponse(self.players, self.dealer)
        for index, tour in enumerate(constants.tours):
            self.dealer.add(self.deck.pick(tour))
            predictions, best_combination, combinations = self.show()
            response.predictions.append(predictions)
            response.best_combinations.append(best_combination)
            response.players_combinations.append(combinations)
        return response

    def show(self) -> Tuple[list[int], Combination, list[Combination]]:
        predictions: list[int] = Predictor(self.deck.cards, self.dealer.cards, [player.cards for player in self.players]).chances
        everybody: list[Player] = self.players + [self.dealer]
        combinations: list[Combination] = [Collection(player.cards + self.dealer.cards).powerful for player in self.players]
        best_combination: Combination = max(combinations, key = lambda x: x.power)
        if self.display:
            for index, player in enumerate(everybody):
                print(f"{player} | {predictions[index]}%\n")
            print(f"{'Best': <10} | {best_combination}\n\n")
        return predictions, best_combination, combinations
