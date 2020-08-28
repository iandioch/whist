from enum import Enum

class CardSuit(Enum):
    HEARTS = 1
    CLUBS = 2
    DIAMONDS = 3
    SPADES = 4

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
