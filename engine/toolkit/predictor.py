import itertools

from engine.toolkit import constants
from engine.toolkit.card import Card
from engine.toolkit.collection import Collection


class Predictor:
    def __init__(self, deck: list[Card], dealer: list[Card], players: list[list[Card]], debug: bool = False):
        self.deck: list[Card] = deck
        self.dealer: list[Card] = dealer
        self.players: list[list[Card]] = players
        self.statistics: list[int] = [0 for _ in range(len(self.players) + 1)]
        self.search_amount: int = (constants.start_cards + sum(constants.tours)) - (len(self.players[0]) + len(self.dealer))
        self.debug = debug

    @property
    def chances(self):
        statistics: list[int] = [0 for _ in range(len(self.players) + 1)]
        for subset in itertools.combinations(self.deck, self.search_amount):
            collections: list[Collection] = [Collection(player + self.dealer + list(subset)) for player in self.players]
            maximum_power = max(collections, key = lambda x: x.power).power
            maximum_count = sum(collection.power == maximum_power for collection in collections)
            maximum_index = next(index for index, collection in enumerate(collections) if collection.power == maximum_power) if maximum_count == 1 else -1
            statistics[maximum_index] += 1

            if self.debug:
                print(f"Dealer: {self.dealer} {subset}")
                for index, player in enumerate(self.players):
                    print(f"Player #{index} {'win' if index == maximum_index else '   '}: {player} {collections[index].powerful}")
                print()

        chances: list[int] = [int(statistic / sum(statistics) * 100) for statistic in statistics]
        chances[-1] = 100 - sum(chances[:-1])
        return chances
