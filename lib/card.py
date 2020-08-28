from enum import Enum

class CardSuit(Enum):
    HEARTS = 1
    CLUBS = 2
    DIAMONDS = 3
    SPADES = 4

    @staticmethod
    def get_suit_name(suit):
        names = {
            CardSuit.HEARTS: "Hearts",
            CardSuit.CLUBS: "Clubs",
            CardSuit.DIAMONDS: "Diamonds",
            CardSuit.SPADES: "Spades",
        }
        return names[suit]

class Card:
    def __init__(self, suit: CardSuit, name: str, value: int):
        self.suit = suit
        self.name = name
        self.value = value

    def __hash__(self):
        return hash((self.suit, self.name, self.value))

    def __eq__(self, other):
        return (self.suit == other.suit and self.name == other.name and
            self.value == other.value)

    def __str__(self):
        return '{} of {}'.format(self.name, CardSuit.get_suit_name(self.suit))
