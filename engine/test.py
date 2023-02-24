from os import listdir

from game.deck import Deck
from toolkit.card import Card
from toolkit.collection import Collection
from toolkit.predictor import Predictor
from vision.detector import Detector


def get_chances(dealer: list[Card], players: list[list[Card]]):
    deck: Deck = Deck()
    for array in players + [dealer]:
        for card in array:
            deck.remove(card)
    return Predictor(deck.cards, dealer, players).chances


class TestCards:

    def test_card_eq(self):
        assert Card(12, "diamonds") == Card(12, "diamonds")

    def test_high_card(self):
        cards = [Card(10, "hearts")]
        collection = Collection(cards)
        assert collection.powerful.name == "high card"
        assert collection.power == 1.1

    def test_pair(self):
        cards = [Card(10, "hearts"), Card(10, "clubs")]
        collection = Collection(cards)
        assert collection.powerful.name == "pair"
        assert collection.power == 2.1

    def test_two_pair(self):
        cards = [Card(9, "diamonds"), Card(9, "clubs"), Card(6, "hearts"), Card(6, "clubs"), Card(10, "spades")]
        collection = Collection(cards)
        assert collection.powerful.name == "two pair"
        assert collection.power == 3.0906

    def test_three(self):
        cards = [Card(6, "hearts"), Card(6, "clubs"), Card(6, "diamonds"), Card(9, "clubs"), Card(10, "spades")]
        collection = Collection(cards)
        assert collection.powerful.name == "three"
        assert collection.power == 4.06

    def test_straight(self):
        cards = [Card(14, "hearts"), Card(2, "clubs"), Card(3, "diamonds"), Card(4, "clubs"), Card(5, "spades")]
        collection = Collection(cards)
        assert collection.powerful.name == "straight"
        assert collection.power == 5.02

        cards = [Card(4, "hearts"), Card(5, "clubs"), Card(6, "clubs"), Card(7, "spades"), Card(8, "diamonds")]
        collection = Collection(cards)
        assert collection.powerful.name == "straight"
        assert collection.power == 5.05

    def test_flush(self):
        cards = [Card(10, "hearts"), Card(6, "hearts"), Card(3, "hearts"), Card(11, "hearts"), Card(7, "hearts")]
        collection = Collection(cards)
        assert collection.powerful.name == "flush"
        assert collection.power == 6.1110070603

    def test_full_house(self):
        cards = [Card(10, "hearts"), Card(10, "clubs"), Card(12, "spades"), Card(12, "hearts"), Card(7, "hearts"), Card(10, "diamonds")]
        collection = Collection(cards)
        assert collection.powerful.name == "full house"
        assert collection.power == 7.1012

    def test_four(self):
        cards = [Card(10, "hearts"), Card(10, "clubs"), Card(12, "spades"), Card(10, "spades"), Card(10, "diamonds")]
        collection = Collection(cards)
        assert collection.powerful.name == "four"
        assert collection.power == 8.1

    def test_straight_flush(self):
        cards = [Card(14, "clubs"), Card(2, "clubs"), Card(3, "clubs"), Card(4, "clubs"), Card(5, "clubs")]
        collection = Collection(cards)
        assert collection.powerful.name == "straight flush"
        assert collection.power == 9.02

        cards = [Card(7, "diamonds"), Card(8, "diamonds"), Card(9, "diamonds"), Card(10, "diamonds"), Card(11, "diamonds")]
        collection = Collection(cards)
        assert collection.powerful.name == "straight flush"
        assert collection.power == 9.08

    def test_statistics_easy(self):
        dealer: list[Card] = [Card(7, "hearts"), Card(8, "clubs"), Card(9, "diamonds")]
        players: list[list[Card]] = [[Card(10, "diamonds"), Card(11, "diamonds")],
                                     [Card(2, "spades"), Card(3, "diamonds")]]
        assert get_chances(dealer, players) == [99, 0, 1]

    def test_statistics_medium(self):
        dealer: list[Card] = [Card(2, "hearts"), Card(10, "clubs"), Card(13, "diamonds")]
        players: list[list[Card]] = [[Card(10, "diamonds"), Card(8, "diamonds")],
                                     [Card(2, "spades"), Card(3, "spades")]]
        assert get_chances(dealer, players) == [83, 16, 1]

    def test_statistics_hard(self):
        dealer: list[Card] = [Card(6, "clubs"), Card(2, "spades"), Card(4, "spades")]
        players: list[list[Card]] = [[Card(10, "spades"), Card(3, "diamonds")],
                                     [Card(12, "spades"), Card(12, "clubs")],
                                     [Card(4, "diamonds"), Card(4, "clubs")]]
        assert get_chances(dealer, players) == [12, 11, 74, 3]

    def test_vision(self):
        divides: int = 2
        filepath: str = "vision/img"
        threshold: float = 0.65
        detector: Detector = Detector()
        for img in listdir(filepath):
            keys_string: str = img.strip(".jpg")
            keys: list[str] = [keys_string[i:i + divides] for i in range(0, len(keys_string), divides)]
            results: dict[str, float] = detector.detect(f"{filepath}/{img}", save = False)
            for key in keys:
                assert results.get(key, 0) > threshold
            assert len([key for key in results.keys() if results[key] > threshold]) == len(keys)
