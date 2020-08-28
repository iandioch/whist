import random

from typing import List

from .card import Card, CardSuit

class CardPile:
    '''A generic ordered set of cards (eg. a hand, a deck).'''
    def __init__(self, cards: List[Card]):
        self.cards = cards

    def shuffle(self):
        random.shuffle(self.cards)

    def __len__(self):
        return len(self.cards)

class CardHand(CardPile):
    def add_card(self, card: Card):
        self.cards.append(card)

class CardDeck(CardPile):
    def deal(self, num_hands, size_of_hand):
        hands = [CardHand([]) for _ in range(num_hands)]
        for _ in range(size_of_hand):
            for hand in hands:
                hand.add_card(self.draw())

    def draw(self):
        return self.cards.pop()

class CardPlayPile(CardPile):
    '''The pile of cards in the middle of the table, added to as people play.'''
    def __init__(self, cards: List[Card]):
        super().__init__(cards)
        self.player_of_card = {}
        self.base_suit = None # The first suit played.

    def add_card(self, card, player):
        if len(self.cards) == 0:
            self.base_suit = card.suit
        self.cards.append(card)
        self.player_of_card[card] = player

    def get_winning_card(self, trump_suit: CardSuit):
        self.cards.sort(key = lambda c: c.value, reversed=True)
        for card in self.cards:
            if card.suit is trump_suit:
                return card
        # No trump suit found
        for card in self.cards:
            if card.suit is self.base_suit:
                return card

    def get_winning_player(self, trump_suit: CardSuit):
        return self.player_of_card[self.winning_card(trump_suit)]



