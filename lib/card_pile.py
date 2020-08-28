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

    def __iter__(self):
        return iter(self.cards)

    def __getitem__(self, i):
        return self.cards[i]


class CardHand(CardPile):

    def add_card(self, card: Card):
        self.cards.append(card)

    def remove_card(self, card: Card):
        self.cards.remove(card)

    def __str__(self):
        return '\n'.join(str(card) for card in self.cards)


class CardDeck(CardPile):

    def deal(self, num_hands, size_of_hand):
        hands = [CardHand([]) for _ in range(num_hands)]
        for _ in range(size_of_hand):
            for hand in hands:
                hand.add_card(self.draw())
        return hands

    def draw(self):
        return self.cards.pop()


class CardPlayPile(CardPile):
    '''The pile of cards in the middle of the table, added to as people play.'''

    def __init__(self, cards: List[Card]):
        super().__init__(cards)
        self.player_of_card = {}
        self.base_suit = None  # The first suit played.

    def add_card(self, card, player):
        if len(self.cards) == 0:
            self.base_suit = card.suit
        self.cards.append(card)
        self.player_of_card[card] = player

    def get_winning_card(self, trump_suit: CardSuit):
        self.cards.sort(key=lambda c: c.value, reverse=True)
        for card in self.cards:
            if card.suit is trump_suit:
                return card
        # No trump suit found
        for card in self.cards:
            if card.suit is self.base_suit:
                return card

    def get_winning_player(self, trump_suit: CardSuit):
        return self.player_of_card[self.get_winning_card(trump_suit)]

    def get_playable_cards(self, hand: CardHand, trump_suit: CardSuit):
        has_base_suit = False
        has_trump_suit = False
        for card in hand:
            if card.suit is self.base_suit:
                has_base_suit = True
            elif card.suit is trump_suit:
                has_trump_suit = True
        if has_base_suit:
            return set(card for card in hand if card.suit is self.base_suit)
        if has_trump_suit:
            return set(card for card in hand if card.suit is trump_suit)
        return set(card for card in hand)
