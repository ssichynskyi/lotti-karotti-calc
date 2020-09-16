# -*- coding: utf-8 -*-
import unittest
from pathlib import Path
from logic.game_engine import LottiGameEngine
from logic.config import Config


class TestPlayField(unittest.TestCase):
    """
    Collection of unittests for Play field class
    """
    def setUp(self):
        # test config to test hole functionality
        config = Config(Path(__file__).parent.joinpath('test_config.yaml'))
        self.test_config = config.options
        print(self.test_config)
        self.number_of_games = 1
        self.game_engine = LottiGameEngine(1, config)
        self.play_field = self.game_engine.play_field

    def test_play_field_init(self):
        # test initialization of a Play Field
        self.game_engine.reset_game()
        self.assertTrue(
            self.play_field.winning_cell.is_winning_cell,
            'Wrong init of winning cell'
        )
        for cell in self.play_field.cells:
            print(f'Cell {cell.number} is hole: {cell.is_hole}')
        self.assertTrue(
            self.play_field.cells[self.test_config['playfield']['holes'][0]].is_hole,
            'Wrong initialization of holes. Cell expected to be hole, but its not'
        )
        for cell in self.play_field.cells:
            if not cell == self.play_field.cells[self.test_config['playfield']['holes'][0]]:
                self.assertFalse(
                    cell.is_hole,
                    'Wrong initialization of holes. Cell expected not to be a hole, but it is'
                )
        cell = self.play_field.starting_cell
        for _ in range(self.test_config['playfield']['number_of_cells']):
            cell = cell.next
        self.assertTrue(
            cell.is_winning_cell,
            'Wrong functionality of next properties'
        )

    def test_carrot_rotation(self):
        self.play_field.rotate_carrot(1)
        self.assertTrue(
            self.play_field.cells[self.test_config['playfield']['holes'][1]].is_hole,
            'Wrong functionality of carrot rotation / holes. Hole expected.'
        )
        for cell in self.play_field.cells:
            if not cell == self.play_field.cells[self.test_config['playfield']['holes'][1]]:
                self.assertFalse(
                    cell.is_hole,
                    'Wrong functionality of carrot rotation / holes. Expected no hole.'
                )

    def test_play_field_reset(self):
        self.play_field.reset_condition()
        self.assertEqual(
            len(self.play_field.cells),
            self.test_config['playfield']['number_of_cells'] + 1
        )
        self.test_play_field_init()
