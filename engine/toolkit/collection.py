import itertools

from engine.toolkit import constants
from engine.toolkit.card import Card
from engine.toolkit.combination import Combination


class Collection:
    def __init__(self, cards: list[Card]):
        self.cards: list[Card] = cards.copy()
        self.combinations: list[Combination] = list()
        self.update()

    def __repr__(self):
        return f"Cards = {self.cards}\n" \
               f"Power combination: {self.combinations[0]}"

    def add(self, cards: list[Card]):
        self.cards.extend(cards)
        self.update()

    @property
    def power(self):
        return self.combinations[0].power

    @property
    def powerful(self):
        return self.combinations[0]

    # Linear complexity - O(n), where n - length of self.cards
    def update(self):
        self.cards.sort(key = lambda x: (x.rank, x.suit))
        self.combinations.clear()
        if len(self.cards) == 0:
            return

        ranks: dict[int, list[Card]] = dict([(rank, list()) for rank in constants.ranks])
        for card in self.cards:
            ranks[card.rank].append(card)

        suites: dict[str, list[Card]] = dict([(suit, list()) for suit in constants.suites])
        for card in self.cards:
            suites[card.suit].append(card)

        # high card
        max_rank_card: Card = max(self.cards, key = lambda x: x.rank)
        self.combinations.append(Combination(tuple([max_rank_card]), "high card"))

        # pair
        for rank, cards in ranks.items():
            if len(cards) == 2:
                self.combinations.append(Combination(tuple(cards), "pair"))

        # two pair
        pairs: list[Combination] = [combination for combination in self.combinations if combination.name == "pair"]
        for index1, pair1 in enumerate(pairs, start = 0):
            for index2, pair2 in enumerate(pairs[index1 + 1:], start = index1 + 1):
                self.combinations.append(Combination((pair1.cards[0], pair1.cards[1], pair2.cards[0], pair2.cards[1]), "two pair"))

        # three
        for rank, cards in ranks.items():
            if len(cards) == 3:
                self.combinations.append(Combination(tuple(cards), "three"))

        # straight
        ace_rank = 14
        straight_length = 5
        straight_ranks: list[list[list[Card]]] = [[ace_rank, ranks[ace_rank]]] + [[rank, cards] for rank, cards in ranks.items()]
        for index in range(len(straight_ranks) - 4):
            found_straight = True
            for i in range(straight_length):
                found_straight = found_straight and len(straight_ranks[index]) > 0
            if not found_straight:
                continue

            for card1 in straight_ranks[index][1]:
                for card2 in straight_ranks[index + 1][1]:
                    for card3 in straight_ranks[index + 2][1]:
                        for card4 in straight_ranks[index + 3][1]:
                            for card5 in straight_ranks[index + 4][1]:
                                self.combinations.append(Combination((card1, card2, card3, card4, card5), "straight"))

        # flush
        for suit, cards in suites.items():
            if len(cards) >= 5:
                for subset in itertools.combinations(cards, 5):
                    self.combinations.append(Combination(subset, "flush"))

        # full house
        threes: list[Combination] = [combination for combination in self.combinations if combination.name == "three"]
        for pair in pairs:
            for three in threes:
                self.combinations.append(Combination((pair.cards[0], pair.cards[1], three.cards[0], three.cards[1], three.cards[2]), "full house"))

        # four
        for rank, cards in ranks.items():
            if len(cards) == 4:
                self.combinations.append(Combination(tuple(cards), "four"))

        # straight flush
        straights: list[Combination] = [combination for combination in self.combinations if combination.name == "straight"]
        for straight in straights:
            if len(set([card.suit for card in straight.cards])) == 1:
                self.combinations.append(Combination(tuple(straight.cards), "straight flush"))

        self.combinations.sort(key = lambda x: -x.power)
