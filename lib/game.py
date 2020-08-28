from .card_pile import CardDeck
from .card import Card, CardSuit

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

    def is_finished(self):
        # TODO(iandioch): impl.
        return False

class Game:
    '''An entire sitting of Whist, comprising of multiple rounds of different
    hand sizes. Mutable.'''
    def __init__(self, num_players):
        self.num_players = num_players
        # Identifier for the current round.
        # Round -1 means the game has not started yet.
        self.round_number = -1
        self.cards_per_round = self.count_cards_per_round()
        self.round = None

    def get_new_deck(self):
        # A 2 of any suit shouldn't come up in practice...
        card_names = ['A', 'K', 'Q', 'J', 10, 9, 8, 7, 6, 5, 4, 3, 2]
        card_values = list(range(13, 1, -1)) # 13, 12, ..., 3, 2

        # There should be 8 cards for each player.
        cards_to_use = 2*self.num_players 

        cards = []
        for i in range(cards_to_use):
            for suit in CardSuit:
                cards.append(Card(suit, card_names[i], card_values[i]))
        return CardDeck(cards)

    def count_cards_per_round(self):
        return (([1]*self.num_players) + [2, 3, 4, 5, 6, 7] +
                ([8]*self.num_players) + [7, 6, 5, 4, 3, 2] +
                ([1]*self.num_players))

    def progress_to_next_round(self):
        if self.round is not None and not self.round.is_finished():
            raise Exception("Tried to progress to new round, but previous round still active.")
        self.round_number += 1
        # TODO(iandioch): Check if game is now finished.
        self.round = Round(self.get_new_deck(), self.num_players,
                self.cards_per_round[self.round_number])
        return self.round
