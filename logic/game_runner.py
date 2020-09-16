# -*- coding: utf-8 -*-


class GameRunner:
    """
    This class represent the game runner which is responsible for:
    running the given game given amount of times and collecting stats
    """
    def __init__(self, game_engine, number_of_games: int):
        self._game_engine = game_engine
        self._current_game_number = 1
        self._number_of_games = number_of_games
        self._game_stats = dict()

    @property
    def number_of_games(self):
        """
        :return: total number of games to run
        """
        return self._number_of_games

    @property
    def current_game_number(self):
        """
        :return: the number of the current game
        """
        return self._current_game_number

    @property
    def statistics(self) -> {str: int}:
        """
        :return: game statistics where key - is id of the player and value - number of wins
        """
        return self._game_stats

    def run_games(self) -> None:
        while self._current_game_number <= self._number_of_games:
            print(f'######################## GAME #{self._current_game_number} ########################')
            winner_id = self._game_engine.run_game()
            if not winner_id:
                key = 'draw'
                print(f'===================== {key.upper()} GAME!!! =====================')
            else:
                key = str(winner_id)
                print(f'================== PLAYER #{key} WINS THE GAME!!! ==================')
            if key in self._game_stats:
                self._game_stats[key] += 1
            else:
                self._game_stats[key] = 1
            self._current_game_number += 1
