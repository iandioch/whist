import argparse

from lib.game import Game

def start_game(args : argparse.Namespace):
    print('Playing a game with {} players.'.format(args.num_players))
    game = Game(args.num_players)

def main():
    parser = argparse.ArgumentParser(description='Play a game of Romanian Whist.')
    parser.add_argument('--num_players', type=int, help='Number of players.')
    args = parser.parse_args()

    start_game(args)


if __name__ == '__main__':
    main()
