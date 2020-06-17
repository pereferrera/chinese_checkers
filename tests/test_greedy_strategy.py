import unittest
from chinese_checkers.cc_game import CCGame
from chinese_checkers.greedy_strategy import GreedyStrategy

from constants import (
    TEST_BOARD_STRATEGY_PLAYER_1_WINS_IN_TWO,
    TEST_BOARD_STRATEGY_PLAYER_2_WINS_IN_TWO,
    TEST_BOARD_STRATEGY_PLAYER_1_WINS_IN_ONE,
    TEST_BOARD_STRATEGY_PLAYER_2_WINS_IN_ONE
)


class TestCCReasoner(unittest.TestCase):

    def test_greedy_strategy_player_1_wins(self):
        game = CCGame(width=5, player_row_spawn=3)
        game.board = TEST_BOARD_STRATEGY_PLAYER_1_WINS_IN_TWO
        strategy = GreedyStrategy(alpha_beta_pruning=False)

        move, score = strategy._select_move(game, 1, 0, -100000, 100000)
        self.assertEqual(100000, score)
        game.apply_move_sequence(move)

        if game.player_turn == 1:
            game.rotate_turn()
        game.rotate_turn()

        move, score = strategy._select_move(game, 1, 0, -100000, 100000)
        self.assertEqual(100000, score)

        game.apply_move_sequence(move)
        self.assertEqual(1, game.state())

    def test_greedy_strategy_player_1_wins_in_one(self):
        game = CCGame(width=5, player_row_spawn=3)
        game.board = TEST_BOARD_STRATEGY_PLAYER_1_WINS_IN_ONE
        strategy = GreedyStrategy(steps=0)

        move, score = strategy._select_move(game, 1, 0, -100000, 100000)
        game.apply_move_sequence(move)
        self.assertEqual(100000, score)
        self.assertEqual(1, game.state())

    def test_greedy_strategy_player_2_wins_in_one(self):
        game = CCGame(width=5, player_row_spawn=3)
        game.board = TEST_BOARD_STRATEGY_PLAYER_2_WINS_IN_ONE
        strategy = GreedyStrategy(steps=0)

        game.rotate_turn()

        move, score = strategy._select_move(game, 2, 0, -100000, 100000)
        game.apply_move_sequence(move)
        self.assertEqual(100000, score)
        self.assertEqual(2, game.state())

    def test_greedy_strategy_player_2_wins(self):
        game = CCGame(width=5, player_row_spawn=3)
        game.board = TEST_BOARD_STRATEGY_PLAYER_2_WINS_IN_TWO
        strategy = GreedyStrategy(steps=1, alpha_beta_pruning=False)
        strategy_0 = GreedyStrategy(steps=0, alpha_beta_pruning=False)

        game.rotate_turn()

        move, score = strategy._select_move(game, 2, 0, -100000, 100000)
        self.assertEqual(100000, score)
        game.apply_move_sequence(move)

        if game.player_turn == 2:
            game.rotate_turn()
        game.rotate_turn()

        move, score = strategy_0._select_move(game, 2, 0, -100000, 100000)
        self.assertEqual(100000, score)

        game.apply_move_sequence(move)
        self.assertEqual(2, game.state())
