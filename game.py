# -*- coding: utf-8 -*-
import argparse
import sys
from pathlib import Path
from logic.config import config
from logic.game_engine import LottiGameEngine
from logic.game_runner import GameRunner


result_log_file = Path(__file__).parent.joinpath('result.txt')


def main(players, number_of_runs) -> None:
    """
    Main method that initializes the game conditions and
    starts the game run
    :param players: number of players in a game
    :param number_of_runs: number of game runs to execute
    :return: None
    """
    sys.stdout = open(result_log_file, "w")
    game_runner = GameRunner(
        LottiGameEngine(players, config),
        number_of_runs
    )
    game_runner.run_games()
    print_stats(game_runner.statistics)


def print_stats(player_stats):
    """
    prints out a given player statistics
    :param player_stats:
    :return: None
    """
    print('\nGAME STATISTICS:')
    for player in sorted(player_stats.keys()):
        if player == 'draw':
            print(f'Draw games: {player_stats[player]}')
        else:
            print(f'Player #{player}: {player_stats[player]}')


if __name__ == "__main__":
    command_line_arg_parser = argparse.ArgumentParser()
    command_line_arg_parser.add_argument(
        'players',
        help='number of players to play the game, typically 2-4',
        type=int
    )
    command_line_arg_parser.add_argument(
        'number_of_games',
        help='number of games to simulate',
        type=int
    )
    args = command_line_arg_parser.parse_args()
    main(args.players, args.number_of_games)
