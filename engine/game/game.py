from engine.game.deck import Deck
from engine.game.player import Player
from engine.toolkit import constants
from engine.toolkit.combination import Combination
from engine.toolkit.collection import Collection
from engine.toolkit.predictor import Predictor
from engine.responses.generator_response import GeneratorResponse


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
            response.predictions.append(self.show())
        return response

    def show(self) -> list[int]:
        chances: list[int] = Predictor(self.deck.cards, self.dealer.cards, [player.cards for player in self.players]).chances
        everybody: list[Player] = self.players + [self.dealer]
        combination: Combination = max([Collection(player.cards + self.dealer.cards).powerful for player in self.players], key = lambda x: x.power)
        if self.display:
            for index, player in enumerate(everybody):
                print(f"{player} | {chances[index]}%\n")
            print(f"{'Best': <10} | {combination}\n\n")
        return chances
