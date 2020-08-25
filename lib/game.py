from card_pile import CardDeck
from card import Card, CardSuit

class Round:
    '''A single round of the game, ie. one or more hands to be won.'''
    def __init__(self, deck: CardDeck, num_players: int, size_of_hand: int):
        self.deck = deck
        self.deck.shuffle()

        self.num_players = num_players
        self.size_of_hand = size_of_hand

        self.trump_card = self.deck.draw()

    def deal(self):
        return self.deck.deal(self.num_players, self.size_of_hand)

class Game:
    '''An entire sitting of Whist, comprising of multiple rounds of different
    hand sizes.'''
    def __init__(self, num_players):
        self.num_players = num_players
