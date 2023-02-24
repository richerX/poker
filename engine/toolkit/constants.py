start_cards = 2
tours = [3, 1, 1]

ranks = {2: "2", 3: "3", 4: "4", 5: "5",
         6: "6", 7: "7", 8: "8", 9: "9", 10: "10",
         11: "J", 12: "Q", 13: "K", 14: "A"}

suites = {"spades": "♠",
          "clubs": "☘",  # ♣
          "diamonds": "💎",  # ♦
          "hearts": "♥"}

combination_powers = {"straight flush": 9,
                      "four": 8,
                      "full house": 7,
                      "flush": 6,
                      "straight": 5,
                      "three": 4,
                      "two pair": 3,
                      "pair": 2,
                      "high card": 1}
