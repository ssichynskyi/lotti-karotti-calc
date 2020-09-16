# -*- coding: utf-8 -*-
import unittest
from logic.player import Player


class TestPlayer(unittest.TestCase):
    """
    Collection of unittests for Player class
    """
    def setUp(self):
        pass

    def test_player_init(self):
        player = Player(player_id=1, rabbits=2, active_rabbits=1, lost_rabbits=1)
        self.assertEqual(len(player.lost_rabbits), 1)
        self.assertEqual(player.lost_rabbits[0].player_id, 1)
        self.assertEqual(player.lost_rabbits[0].number, 1)
        print('lost rabbits are ok')
        self.assertEqual(len(player.active_rabbits), 1)
        self.assertEqual(player.active_rabbits[0].player_id, 1)
        self.assertEqual(player.active_rabbits[0].number, 2)
        self.assertEqual(len(player.ready_rabbits), 0)

    def test_player_reset(self):
        player = Player(player_id=1, rabbits=2, active_rabbits=1, lost_rabbits=1)
        player.reset_condition()
        self.assertEqual(len(player.lost_rabbits), 0, 'number of lost rabbits expected 0')
        self.assertLessEqual(len(player.active_rabbits), 1, 'number of act. rabbits expected <= 1')
        self.assertLessEqual(len(player.ready_rabbits), 2, 'number of ready rabbits expected <= 2')
        self.assertEqual(len(player.ready_rabbits) + len(player.active_rabbits), 2)

    def test_player_drop_rabbit(self):
        player = Player(player_id=1, rabbits=2, active_rabbits=1, lost_rabbits=1)
        player.drop_active_rabbit()
        self.assertEqual(len(player.lost_rabbits), 2)
        self.assertEqual(len(player.active_rabbits), 0)
        self.assertEqual(len(player.ready_rabbits), 0)

    def test_player_out_of_the_game(self):
        player = Player(player_id=1, rabbits=0)
        self.assertFalse(player.is_active)
        self.assertEqual(player.get_active_rabbit(), None)
