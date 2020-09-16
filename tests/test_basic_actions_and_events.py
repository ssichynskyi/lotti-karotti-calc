# -*- coding: utf-8 -*-
import unittest
from pathlib import Path
from logic.game_engine import LottiGameEngine
from logic.game_runner import GameRunner
from logic.config import Config
from logic.stack import Card


class TestGameEngineAndRunner(unittest.TestCase):
    """
    Set of tests to check main game actions and rules
    """
    def setUp(self):
        # test config to test hole functionality
        self.test_config = Config(Path(__file__).parent.joinpath('test_config.yaml'))
        self.number_of_games = 1
        self.game_engine = LottiGameEngine(1, self.test_config)

    def test_rabbit_move(self):
        self.game_engine.reset_game()
        player = self.game_engine.players[0]
        self.game_engine.perform_player_action(player, Card(1, 0))
        self.assertTrue(self.game_engine.is_busy(self.game_engine.play_field.cells[1]))

    def test_rabbit_jumping_over_hole_and_reach_winning_cell(self):
        self.game_engine.reset_game()
        player = self.game_engine.players[0]
        winner = self.game_engine.perform_player_action(player, Card(4, 0))
        self.assertEqual(winner, player)

    def test_rabbit_falls_into_existing_hole(self):
        self.game_engine.reset_game()
        player = self.game_engine.players[0]
        rabbit = player.get_active_rabbit()
        self.game_engine.perform_player_action(player, Card(2, 0))
        self.assertEqual(player.lost_rabbits[0], rabbit)
        self.assertEqual(player.get_active_rabbit().number, 2)

    def test_rabbit_falls_into_new_hole(self):
        self.game_engine.reset_game()
        player = self.game_engine.players[0]
        rabbit = player.get_active_rabbit()
        self.game_engine.perform_player_action(player, Card(1, 0))
        self.game_engine.perform_player_action(player, Card(0, 1))
        self.assertEqual(player.lost_rabbits[0], rabbit)
        self.assertEqual(player.get_active_rabbit().number, 2)

    def test_draw_game(self):
        self.game_engine.reset_game()
        player = self.game_engine.players[0]
        required_steps = self.test_config.options['playfield']['holes'][0]
        # send all rabbits to a opened hole
        winner = player
        for _ in range(self.test_config.options['rabbits_per_player']):
            winner = self.game_engine.perform_player_action(player, Card(required_steps, 0))
        self.assertEqual(winner, None)

    def test_no_holes_case(self):
        self.game_engine.reset_game()
        player = self.game_engine.players[0]
        # rotate to reach end position e.g. no holes
        rotations = len(self.test_config.options['playfield']['holes']) - 1
        self.game_engine.perform_player_action(player, Card(0, rotations))
        winner = None
        for _ in range(3):
            winner = self.game_engine.perform_player_action(player, Card(1, 0))
        self.assertEqual(winner, player)

    def test_rabbit_jumps_over_other_rabbits(self):
        self.game_engine = LottiGameEngine(3, self.test_config)
        player_one = self.game_engine.players[0]
        player_two = self.game_engine.players[1]
        player_three = self.game_engine.players[2]
        self.game_engine.perform_player_action(player_one, Card(0, 2))
        self.game_engine.perform_player_action(player_one, Card(1, 0))
        self.game_engine.perform_player_action(player_two, Card(1, 0))
        self.game_engine.perform_player_action(player_three, Card(1, 0))
        for cell in self.game_engine.play_field.cells:
            self.assertTrue(self.game_engine.is_busy(cell))

    def test_game_runner(self):
        test_config = Config(Path(__file__).parent.joinpath('test_config.yaml'))
        test_config.options['playfield']['holes'] = [4]
        self.game_engine = LottiGameEngine(2, test_config)
        player_one = self.game_engine.players[0]
        game_runner = GameRunner(self.game_engine, 1)
        game_runner.run_games()
        self.assertEqual(game_runner.statistics[str(player_one.id)], 1)


if __name__ == '__main__':
    unittest.main()
