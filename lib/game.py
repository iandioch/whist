from .card_pile import CardDeck, CardPlayPile
from .card import Card, CardSuit
from .player import Player

from collections import defaultdict
from enum import Enum, auto
from typing import List

class RoundState(Enum):
    # TODO(iandioch): Add AWAITING_BID
    # Waiting for round.active_player to put a card down.
    AWAITING_TURN = auto()
    # All players have put down a card, should call round_manager.finish_hand().
    HAND_FINISHED = auto()
    # All hands of the round have been finished, move on!
    ROUND_FINISHED = auto()


class Round:
    '''A single round of the game, ie. one or more hands to be won. Mutable'''
    def __init__(self, deck: CardDeck, players: List[Player], size_of_hand: int):
        self.deck = deck
        self.deck.shuffle()
        self.players = players 
        self.size_of_hand = size_of_hand
        self.hands_remaining = size_of_hand

        # TODO(iandioch): It shouldn't always start with the first player.
        self.active_player = players[0]
        self.hands = {}
        for i, hand in enumerate(self.deal()):
            self.hands[players[i]] = hand
        
        self.trump_card = self.deck.draw()
        self.trump_suit = self.trump_card.suit
        self.play_pile = CardPlayPile([])

        # Contains the mapping Player:List[CardPlayPile]
        self.hands_won = defaultdict(list)

    def deal(self):
        return self.deck.deal(len(self.players), self.size_of_hand)

    def is_finished(self):
        # TODO(iandioch): remove.
        return False

    def _next_player(self, current_player):
        choose_next_player = False
        for player in self.players:
            if player == current_player:
                choose_next_player = True
                continue
            if choose_next_player:
                return player
        # Must be the first player.
        return self.players[0]

    def progress_to_next_player(self):
        self.active_player = self._next_player(self.active_player)

class RoundManager:
    '''Handles game events, actions, etc. in a round.'''
    def __init__(self, game_round: Round):
        self.round = game_round
        self.state = RoundState.AWAITING_TURN

    def finish_hand(self):
        winner = self.round.play_pile.get_winning_player(self.round.trump_suit)
        self.round.hands_won[winner].append(self.round.play_pile)
        self.round.play_pile = CardPlayPile([])
        self.round.turn = winner

        self.round.hands_remaining -= 1
        if self.round.hands_remaining == 0:
            self.state = RoundState.ROUND_FINISHED
        else:
            self.state = RoundState.AWAITING_TURN

    def play_card(self, card, player):
        if player != self.round.active_player:
            raise Exception('It is not {}\'s turn, it is {}\'s.'.format(
                player.identifier, self.round.active_player.identifier))
        # TODO(iandioch): Check 'player' is actually holding 'card'
        # TODO(iandioch): Check 'card' is a legal move (ie. matches base suit or trump, etc.)
        # TODO(iandioch): Remove 'card' from 'player's hand.
        self.round.play_pile.add_card(card, player)
        if len(self.round.play_pile) == len(self.round.players):
            # All players have put a card in, so this hand is over.
            self.state = RoundState.HAND_FINISHED
            return 
        else:
            # It is the next player's turn to put down a card.
            self.state = RoundState.AWAITING_TURN
            self.round.progress_to_next_player()

class Game:
    '''An entire sitting of Whist, comprising of multiple rounds of different
    hand sizes. Mutable.'''
    def __init__(self, players: List[Player]):
        self.players = players
        self.num_players = len(self.players)
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
        self.round_number += 1
        # TODO(iandioch): Check if game is now finished.
        self.round = Round(self.get_new_deck(), self.players,
                self.cards_per_round[self.round_number])
        return self.round
