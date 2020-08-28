import argparse

from lib.game import Game, RoundManager, RoundState
from lib.player import Player

def start_game(args : argparse.Namespace):
    print('Playing a game with {} players.'.format(args.num_players))
    players = [Player('Player {}'.format(i+1)) for i in range(args.num_players)]
    game = Game(players)
    while True:
        round_manager = RoundManager(game.progress_to_next_round())
        while True:
            state = round_manager.state
            if state == RoundState.ROUND_FINISHED:
                break
            elif state == RoundState.AWAITING_TURN:
                print('Awaiting turn from player {}.'.format(
                    game.round.active_player.identifier))
                # TODO(iandioch): Render hand, allow some input, etc.
                turn = input()
            elif state == RoundState.HAND_FINISHED:
                round_manager.finish_hand()
                print('Hand finished!')
        # TODO(iandioch): Handle finished game.

def main():
    parser = argparse.ArgumentParser(description='Play a game of Romanian Whist.')
    parser.add_argument('--num_players', type=int, help='Number of players.')
    args = parser.parse_args()

    start_game(args)


if __name__ == '__main__':
    main()
