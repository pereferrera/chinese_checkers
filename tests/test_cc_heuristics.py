import unittest

from chinese_checkers.cc_game import CCGame
from chinese_checkers.cc_heuristics import combined_vertical_advance

from constants import (
    TEST_BOARD_VA_1_1, TEST_BOARD_VA_1_2,
    TEST_BOARD_VA_2_1, TEST_BOARD_VA_2_2
)

class TestCCHeuristics(unittest.TestCase):

    def test_combined_vertical_advance_symmetry(self):
        game = CCGame(width=5)
        self.assertEqual(combined_vertical_advance(game, 1),
                         combined_vertical_advance(game, 2))
        self.assertEqual(8, combined_vertical_advance(game, 1))

    def test_combined_vertical_advance_player_1(self):
        game_1 = CCGame(width=5)
        game_2 = CCGame(width=5)
        game_1.board = TEST_BOARD_VA_1_1
        game_2.board = TEST_BOARD_VA_1_2
        self.assertTrue(combined_vertical_advance(game_1, 1) <
                        combined_vertical_advance(game_2, 1))
        
    def test_combined_vertical_advance_player_2(self):
        game_1 = CCGame(width=5)
        game_2 = CCGame(width=5)
        game_1.board = TEST_BOARD_VA_2_1
        game_2.board = TEST_BOARD_VA_2_2
        self.assertTrue(combined_vertical_advance(game_1, 2) <
                        combined_vertical_advance(game_2, 2))