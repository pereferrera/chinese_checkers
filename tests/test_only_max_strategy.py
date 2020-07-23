import unittest

from chinese_checkers.game import CCGame
from chinese_checkers.strategy.only_max_strategy import OnlyMaxStrategy
from constants import (
    TEST_BOARD_STRATEGY_PLAYER_1_WINS_IN_TWO,
    TEST_BOARD_STRATEGY_PLAYER_2_WINS_IN_TWO,
)
from chinese_checkers.heuristic.heuristics import CombinedVerticalAdvance


class TestOnlyMaxStrategy(unittest.TestCase):

    def test_player_1_wins(self):
        game = CCGame(width=5, player_row_span=3)
        game.board = TEST_BOARD_STRATEGY_PLAYER_1_WINS_IN_TWO
        strategy = OnlyMaxStrategy(steps=1, player=1,
                                   heuristic=CombinedVerticalAdvance())

        move, score = strategy._select_move(game, 0)
        self.assertEqual(50000, score)
        game.apply_move_sequence(move)
        game.rotate_turn()

        move, score = strategy._select_move(game, 0)
        self.assertEqual(100000, score)

        game.apply_move_sequence(move)

        self.assertEqual(1, game.state())

    def test_player_2_wins(self):
        game = CCGame(width=5, player_row_span=3)
        game.board = TEST_BOARD_STRATEGY_PLAYER_2_WINS_IN_TWO
        strategy = OnlyMaxStrategy(steps=1, player=2,
                                   heuristic=CombinedVerticalAdvance())

        game.rotate_turn()

        move, score = strategy._select_move(game, 0)
        self.assertEqual(50000, score)
        game.apply_move_sequence(move)

        game.rotate_turn()

        move, score = strategy._select_move(game, 0)
        self.assertEqual(100000, score)

        game.apply_move_sequence(move)
        self.assertEqual(2, game.state())
