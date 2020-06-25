import unittest
from chinese_checkers.cc_game import CCGame
from chinese_checkers.only_max_strategy import OnlyMaxStrategy

from constants import (
    TEST_BOARD_STRATEGY_PLAYER_1_WINS_IN_TWO,
    TEST_BOARD_STRATEGY_PLAYER_2_WINS_IN_TWO,
)


class TestOnlyMaxStrategy(unittest.TestCase):

    def test_player_1_wins(self):
        game = CCGame(width=5, player_row_spawn=3)
        game.board = TEST_BOARD_STRATEGY_PLAYER_1_WINS_IN_TWO
        strategy = OnlyMaxStrategy(steps=1, player=1)

        game.pretty_print_board()

        move, score = strategy._select_move(game, 0)
        self.assertEqual(100000, score)
        game.apply_move_sequence(move)
        game.pretty_print_board()
        game.rotate_turn()

        move, score = strategy._select_move(game, 0)
        self.assertEqual(100000, score)

        game.apply_move_sequence(move)
        game.pretty_print_board()

        self.assertEqual(1, game.state())

    @unittest.skip
    def test_player_2_wins(self):
        game = CCGame(width=5, player_row_spawn=3)
        game.board = TEST_BOARD_STRATEGY_PLAYER_2_WINS_IN_TWO
        strategy = OnlyMaxStrategy(steps=1, player=2)

        game.rotate_turn()

        move, score = strategy._select_move(game, 0)
        self.assertEqual(100000, score)
        game.apply_move_sequence(move)

        game.rotate_turn()

        move, score = strategy._select_move(game, 0)
        self.assertEqual(100000, score)

        game.apply_move_sequence(move)
        game.pretty_print_board()
        self.assertEqual(2, game.state())
