import unittest

from chinese_checkers.cc_game import CCGame
from chinese_checkers.cc_heuristics import (
    combined_vertical_advance,
    inv_squared_sum_dest_corner,
    inv_squared_sum_center_line
)

from constants import (
    TEST_BOARD_VA_1_1, TEST_BOARD_VA_1_2,
    TEST_BOARD_VA_2_1, TEST_BOARD_VA_2_2,
    TEST_BOARD_SQUARED_SUM, TEST_BOARD_SQUARED_SUM_ZERO,
    TEST_BOARD_CENTER_LINE
)


class TestCCHeuristics(unittest.TestCase):

    def test_combined_vertical_advance_symmetry(self):
        game = CCGame(width=5)
        self.assertEqual(combined_vertical_advance(game, 1),
                         combined_vertical_advance(game, 2))

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

    def test_inv_squared_sum_dest_corner(self):
        game = CCGame(width=5)
        game.board = TEST_BOARD_SQUARED_SUM
        self.assertTrue(inv_squared_sum_dest_corner(game, 1) <
                        inv_squared_sum_dest_corner(game, 2))

    def inv_squared_sum_dest_corner_zero(self):
        game = CCGame(width=5)
        game.board = TEST_BOARD_SQUARED_SUM_ZERO
        self.assertEqual(inv_squared_sum_dest_corner(game, 1), 0)
        self.assertEqual(inv_squared_sum_dest_corner(game, 2), 0)

    def test_inv_squared_sum_center_line(self):
        game = CCGame(width=5)
        game.board = TEST_BOARD_CENTER_LINE
        self.assertTrue(inv_squared_sum_center_line(game, 2) <
                        inv_squared_sum_center_line(game, 1))
