import argparse

from lib.game import Game, RoundManager, RoundState
from lib.player import Player

def debug_log(s):
    print('- [CLI] {}'.format(s))

def print_active_hand(game):
    print('\n\nCurrent hand:')
    playable_cards = game.round.play_pile.get_playable_cards(
        game.round.hands[game.round.active_player],
        game.round.trump_suit)
    playable_indexes = set()
    for i, card in enumerate(game.round.hands[game.round.active_player]):
        playable = (card in playable_cards) or (
            len(game.round.play_pile) == 0)
        if playable:
            playable_indexes.add(i)
        print('[{}]: {} {}'.format(i, card,
                                   '' if playable else '(not playable)'))



def start_game(args: argparse.Namespace):
    print('Playing a game with {} players.'.format(args.num_players))
    players = [Player('Player {}'.format(i + 1))
               for i in range(args.num_players)]
    game = Game(players)
    while True:
        print('-' * 10)
        print('New round!')
        print('Shuffling, dealing, thinking...')
        print('-' * 10)
        round_manager = RoundManager(game.progress_to_next_round())
        print('Trump card is {}'.format(game.round.trump_card))
        while True:
            state = round_manager.state
            if state == RoundState.ROUND_FINISHED:
                debug_log('ROUND_FINISHED')
                break
            elif state == RoundState.AWAITING_TURN:
                debug_log('AWAITING_TURN')
                print('\nAwaiting turn from player {}.'.format(
                    game.round.active_player.identifier))

                print_active_hand(game)

                choice = None
                while True:
                    choice_str = input('Choose a card index: ')
                    try:
                        choice = int(choice_str)
                    except Exception as e:
                        print(e)
                        print('Please choose a valid card index.')
                        continue
                    if choice not in playable_indexes:
                        print('Please choose a valid card index.')
                    else:
                        break
                card = game.round.hands[game.round.active_player][choice]
                print('Chose to play: {}'.format(card))
                round_manager.play_card(card, game.round.active_player)
            elif state == RoundState.HAND_FINISHED:
                debug_log('HAND_FINISHED')
                round_manager.finish_hand()
                print('Hand finished!')
            elif state == RoundState.AWAITING_BID:
                debug_log('AWAITING_BID')
                print('\nAwaiting bid from player {}.'.format(
                    game.round.active_player.identifier))

                print_active_hand(game)

                choice = None
                while True:
                    bid_str = input('Make a bid: ')
                    try:
                        bid = int(bid_str)
                        round_manager.make_bid(game.round.active_player, bid)
                        break
                    except Exception as e:
                        print(e)
                        print('Please choose a valid bid.')
                        continue
        # TODO(iandioch): Handle finished game.
        print('Round finished!')


def main():
    parser = argparse.ArgumentParser(
        description='Play a game of Romanian Whist.')
    parser.add_argument('--num_players', type=int, help='Number of players.')
    args = parser.parse_args()

    start_game(args)


if __name__ == '__main__':
    main()
