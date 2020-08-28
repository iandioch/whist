from .card_pile import CardDeck, CardPlayPile
from .card import Card, CardSuit
from .player import Player
from .event import EventLog, EventType

from collections import defaultdict
from enum import Enum, auto
from typing import List


class RoundState(Enum):
    # TODO(iandioch): Add AWAITING_BID
    # Waiting for round.active_player to put a card down.
    AWAITING_TURN = auto()
    # All players have put down a card, should call
    # round_manager.finish_hand().
    HAND_FINISHED = auto()
    # All hands of the round have been finished, move on!
    ROUND_FINISHED = auto()


class Round:
    '''A single round of the game, ie. one or more hands to be won. Mutable'''

    def __init__(self, deck: CardDeck, players: List[Player], size_of_hand: int,
                 event_log: EventLog, starting_player: Player):
        self.event_log = event_log
        self.deck = deck
        self.deck.shuffle()
        self.players = players
        self.size_of_hand = size_of_hand
        self.hands_remaining = size_of_hand

        self.active_player = starting_player
        self.hands = {}
        for i, hand in enumerate(self.deal()):
            self.hands[players[i]] = hand

        self.trump_card = self.deck.draw()
        self.event_log.add_event(EventType.NEW_TRUMP_CARD, data={
            'card': str(self.trump_card)
        })
        self.trump_suit = self.trump_card.suit
        self.play_pile = CardPlayPile([])

        # Contains the mapping Player:List[CardPlayPile]
        self.hands_won = defaultdict(list)

    def deal(self):
        self.event_log.add_event(EventType.DEAL, data={
            'hand_size': self.size_of_hand,
            'num_hands': len(self.players)
        })
        return self.deck.deal(len(self.players), self.size_of_hand)

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
        next_player = self._next_player(self.active_player)
        self.event_log.add_event(EventType.TURN_CHANGED, data={
            'new_active_player': next_player.identifier
        })
        self.active_player = next_player


class RoundManager:
    '''Handles game events, actions, etc. in a round.'''

    def __init__(self, game_round: Round):
        self.round = game_round
        self.state = RoundState.AWAITING_TURN
        self.event_log = self.round.event_log

    def finish_hand(self):
        winner = self.round.play_pile.get_winning_player(self.round.trump_suit)
        self.round.hands_won[winner].append(self.round.play_pile)
        self.round.play_pile = CardPlayPile([])
        self.round.turn = winner
        self.event_log.add_event(EventType.HAND_FINISHED, data={
            'winner': winner.identifier
        })

        self.round.hands_remaining -= 1
        if self.round.hands_remaining == 0:
            self.state = RoundState.ROUND_FINISHED
            self.event_log.add_event(EventType.ROUND_FINISHED)
        else:
            self.state = RoundState.AWAITING_TURN

    def play_card(self, card, player):
        if player != self.round.active_player:
            raise Exception('It is not {}\'s turn, it is {}\'s.'.format(
                player.identifier, self.round.active_player.identifier))
        playable_cards = self.round.play_pile.get_playable_cards(
            self.round.hands[player], self.round.trump_suit)
        is_first_player = len(self.round.play_pile) == 0
        if card not in playable_cards and not is_first_player:
            raise Exception('This card is not a playable card from this hand')
        self.round.play_pile.add_card(card, player)
        self.event_log.add_event(EventType.CARD_PLAYED, data={
            'player': player.identifier,
            'card': str(card)
        })
        self.round.hands[player].remove_card(card)
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
        self.event_log = EventLog()
        self.event_log.add_event(EventType.NEW_GAME, "New game started", data={
            'num_players': self.num_players
        })

    def get_new_deck(self):
        # A 2 of any suit shouldn't come up in practice...
        card_names = ['A', 'K', 'Q', 'J', 10, 9, 8, 7, 6, 5, 4, 3, 2]
        card_values = list(range(13, 1, -1))  # 13, 12, ..., 3, 2

        # There should be 8 cards for each player.
        cards_to_use = 2 * self.num_players

        cards = []
        for i in range(cards_to_use):
            for suit in CardSuit:
                cards.append(Card(suit, card_names[i], card_values[i]))
        return CardDeck(cards)

    def count_cards_per_round(self):
        return (([1] * self.num_players) + [2, 3, 4, 5, 6, 7] +
                ([8] * self.num_players) + [7, 6, 5, 4, 3, 2] +
                ([1] * self.num_players))

    def progress_to_next_round(self):
        self.round_number += 1
        starting_player = self.players[self.round_number % len(self.players)]
        # TODO(iandioch): Check if game is now finished.
        self.round = Round(self.get_new_deck(), self.players,
                           self.cards_per_round[
                               self.round_number], self.event_log,
                           starting_player)
        self.event_log.add_event(EventType.NEW_ROUND, data={
            'starting_player': starting_player.identifier,
            'round_number': self.round_number,
            'num_cards': self.cards_per_round[self.round_number],
        })
        return self.round
