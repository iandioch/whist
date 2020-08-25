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
