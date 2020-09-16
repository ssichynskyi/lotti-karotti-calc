# -*- coding: utf-8 -*-
import copy
import unittest
from unittest.mock import MagicMock
from logic.stack import Stack


class TestStack(unittest.TestCase):
    """
    Collection of unittests for Stack class
    """
    def setUp(self):
        mock_config_stack_one_card = {
            'test_card': {
                'move': 4,
                'rotate': 2,
                'qtty': 1
            }
        }
        mock_config_stack_zero_cards = copy.deepcopy(mock_config_stack_one_card)
        mock_config_stack_zero_cards['test_card']['qtty'] = 0

        self.test_stack_one_card = Stack(mock_config_stack_one_card)
        self.test_stack_zero_cards = Stack(mock_config_stack_zero_cards)

    def test_card_generation(self):
        self.assertEqual(self.test_stack_one_card.cards[0].move, 4)
        self.assertEqual(self.test_stack_one_card.cards[0].rotate, 2)

    def test_number_of_cards_in_stack(self):
        self.assertEqual(len(self.test_stack_one_card.cards), 1)
        self.assertEqual(len(self.test_stack_zero_cards.cards), 0)

    def test_generate_new_is_called(self):
        self.test_stack_zero_cards.generate_new = MagicMock()
        with self.assertRaises(IndexError):
            self.test_stack_zero_cards.pull_card()
        self.test_stack_zero_cards.generate_new.assert_called_with()

    def test_random_selects_last_card(self):
        self.assertEqual(self.test_stack_one_card.pull_card().move, 4)


if __name__ == '__main__':
    unittest.main()
