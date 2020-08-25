import random

from typing import List

from card import Card, CardSuit

class CardPile:
    '''A generic ordered set of cards (eg. a hand, a deck).'''
    def __init__(self, cards: List[Card]):
        self.cards = cards

    def shuffle(self):
        random.shuffle(self.cards)

class CardHand(CardPile):
    def add_card(self, card: Card):
        self.cards.append(card)

class CardDeck(CardPile):
    def deal(self, num_hands, size_of_hand):
        hands = [CardHand() for _ in range(num_hands)]
        for _ in range(size_of_hand):
            for hand in hands:
                hand.add_card(self.draw_card())

    def draw_card(self):
        return self.cards.pop()
