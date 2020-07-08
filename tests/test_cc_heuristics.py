import unittest

from chinese_checkers.cc_game import CCGame

from constants import (
    TEST_BOARD_VA_1_1, TEST_BOARD_VA_1_2,
    TEST_BOARD_VA_2_1, TEST_BOARD_VA_2_2,
    TEST_BOARD_SQUARED_SUM, TEST_BOARD_SQUARED_SUM_ZERO,
    TEST_BOARD_CENTER_LINE
)
from chinese_checkers.cc_movement import CCMovement
from chinese_checkers.cc_heuristics import CombinedVerticalAdvance,\
    InvSquaredSumCenterLine, InvSquaredSumDestCorner, CombinedHeuristic
from chinese_checkers.oc_heuristic import OptimizedCombinedHeuristic


class TestCCHeuristics(unittest.TestCase):

    def test_combined_vertical_advance_symmetry(self):
        game = CCGame(width=5)
        heuristic = CombinedVerticalAdvance()
        self.assertEqual(heuristic.value(game, 1),
                         heuristic.value(game, 2))

    def test_combined_vertical_advance_player_1(self):
        game_1 = CCGame(width=5)
        game_2 = CCGame(width=5)
        game_1.board = TEST_BOARD_VA_1_1
        game_2.board = TEST_BOARD_VA_1_2
        heuristic = CombinedVerticalAdvance()
        self.assertTrue(heuristic.value(game_1, 1) <
                        heuristic.value(game_2, 1))

    def test_combined_vertical_advance_player_2(self):
        game_1 = CCGame(width=5)
        game_2 = CCGame(width=5)
        game_1.board = TEST_BOARD_VA_2_1
        game_2.board = TEST_BOARD_VA_2_2
        heuristic = CombinedVerticalAdvance()
        self.assertTrue(heuristic.value(game_1, 2) <
                        heuristic.value(game_2, 2))

    def test_inv_squared_sum_dest_corner(self):
        game = CCGame(width=5)
        game.board = TEST_BOARD_SQUARED_SUM
        heuristic = InvSquaredSumDestCorner()
        self.assertTrue(heuristic.value(game, 1) <
                        heuristic.value(game, 2))

    def inv_squared_sum_dest_corner_zero(self):
        game = CCGame(width=5)
        game.board = TEST_BOARD_SQUARED_SUM_ZERO
        heuristic = InvSquaredSumDestCorner()
        self.assertEqual(heuristic.value(game, 1), 0)
        self.assertEqual(heuristic.value(game, 2), 0)

    def test_inv_squared_sum_center_line(self):
        game = CCGame(width=5)
        game.board = TEST_BOARD_CENTER_LINE
        heuristic = InvSquaredSumCenterLine()
        self.assertTrue(heuristic.value(game, 2) <
                        heuristic.value(game, 1))

    def test_combined_heuristic(self):
        game_1 = CCGame(width=5)
        game_2 = CCGame(width=5)
        game_1.board = TEST_BOARD_VA_2_1
        game_2.board = TEST_BOARD_VA_2_2
        heuristic = CombinedVerticalAdvance()
        self.assertTrue(heuristic.value(game_1, 2) <
                        heuristic.value(game_2, 2))

    def test_optimized_combined_heuristic(self):
        heuristic = CombinedHeuristic()
        optimized_heuristic = OptimizedCombinedHeuristic()

        game_1 = CCGame(width=5, visitors=[optimized_heuristic])

        def heuristics_agree():
            for player in [1, 2]:
                self.assertAlmostEqual(heuristic.value(game_1, player),
                                       optimized_heuristic.value(game_1,
                                                                 player),
                                       2)

        game_1.move(2, 1, CCMovement.LS)
        heuristics_agree()

        game_1.move(7, 1, CCMovement.RN)
        heuristics_agree()

        game_1.undo_last_move()
        game_1.rotate_turn()
        heuristics_agree()

        game_1.undo_last_move()
        heuristics_agree()
