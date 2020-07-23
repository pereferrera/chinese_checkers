import unittest
from chinese_checkers.game import CCGame
from chinese_checkers.strategy.min_max_strategy import MinMaxStrategy

from constants import (
    TEST_BOARD_STRATEGY_PLAYER_1_WINS_IN_TWO,
    TEST_BOARD_STRATEGY_PLAYER_2_WINS_IN_TWO,
    TEST_BOARD_STRATEGY_PLAYER_1_WINS_IN_ONE,
    TEST_BOARD_STRATEGY_PLAYER_2_WINS_IN_ONE,
    TEST_BOARD_VA_1_1,
    TEST_BOARD_VA_2_2,
    TEST_BOARD_END_GAME)


class TestMinMaxStrategy(unittest.TestCase):

    def test_player_1_wins(self):
        game = CCGame(width=5, player_row_span=3)
        game.board = TEST_BOARD_STRATEGY_PLAYER_1_WINS_IN_TWO
        strategy = MinMaxStrategy(alpha_beta_pruning=False)

        move, score = strategy._select_move(game, 1, 0, -100000, 100000)
        self.assertTrue(score > 1000)
        game.apply_move_sequence(move)

        game.rotate_turn()

        move, score = strategy._select_move(game, 1, 0, -100000, 100000)
        self.assertEqual(100000, score)

        game.apply_move_sequence(move)
        self.assertEqual(1, game.state())

    def test_player_1_wins_in_one(self):
        game = CCGame(width=5, player_row_span=3)
        game.board = TEST_BOARD_STRATEGY_PLAYER_1_WINS_IN_ONE
        strategy = MinMaxStrategy(steps=0)

        move, score = strategy._select_move(game, 1, 0, -100000, 100000)
        game.apply_move_sequence(move)
        self.assertEqual(100000, score)
        self.assertEqual(1, game.state())

    def test_player_2_wins_in_one(self):
        game = CCGame(width=5, player_row_span=3)
        game.board = TEST_BOARD_STRATEGY_PLAYER_2_WINS_IN_ONE
        strategy = MinMaxStrategy(steps=0)

        game.rotate_turn()

        move, score = strategy._select_move(game, 2, 0, -100000, 100000)
        game.apply_move_sequence(move)
        self.assertEqual(100000, score)
        self.assertEqual(2, game.state())

    def test_player_2_wins(self):
        game = CCGame(width=5, player_row_span=3)
        game.board = TEST_BOARD_STRATEGY_PLAYER_2_WINS_IN_TWO
        strategy = MinMaxStrategy(steps=1, alpha_beta_pruning=False)
        strategy_0 = MinMaxStrategy(steps=0, alpha_beta_pruning=False)

        game.rotate_turn()

        move, score = strategy._select_move(game, 2, 0, -100000, 100000)
        self.assertTrue(score > 1000)
        game.apply_move_sequence(move)

        game.rotate_turn()

        move, score = strategy_0._select_move(game, 2, 0, -100000, 100000)
        self.assertTrue(score > 1000)

        game.apply_move_sequence(move)
        self.assertEqual(2, game.state())

    def test_use_only_max_beginning_game(self):
        game = CCGame(width=5, player_row_span=3)
        game.board = TEST_BOARD_VA_2_2
        strat = MinMaxStrategy(steps=0, alpha_beta_pruning=False)
        self.assertTrue(strat._use_only_max(game))

    def test_use_only_max_end_game(self):
        game = CCGame(width=5, player_row_span=2)
        game.board = TEST_BOARD_END_GAME
        strat = MinMaxStrategy(steps=0, alpha_beta_pruning=False)
        self.assertTrue(strat._use_only_max(game))

    def test_use_only_max_false(self):
        game = CCGame(width=5, player_row_span=3)
        game.board = TEST_BOARD_VA_1_1
        strat = MinMaxStrategy(steps=0, alpha_beta_pruning=False)
        self.assertFalse(strat._use_only_max(game))

    def test_alpha_beta_prunning(self):
        """assert that using alpha-beta prunning doesn't alter
        the choice of movements"""
        game = CCGame(width=5, player_row_span=3)
        strat_ab = MinMaxStrategy(steps=1, alpha_beta_pruning=True)
        strat_no_ab = MinMaxStrategy(steps=1, alpha_beta_pruning=False)

        N_STEPS = 10

        for _ in range(0, N_STEPS):
            m_ab = strat_ab.select_move(game, game.player_turn)
            m_no_ab = strat_no_ab.select_move(game, game.player_turn)

            self.assertEqual(m_ab, m_no_ab)
            game.apply_move_sequence(m_ab)

    def test_transposition_table(self):
        """assert that using a transposition table doesn't alter
        the choice of movements"""
        game = CCGame(width=5, player_row_span=3)
        strat_tt = MinMaxStrategy(steps=1,
                                  alpha_beta_pruning=False,
                                  transposition_table=True)
        strat_no_tt = MinMaxStrategy(steps=1,
                                     alpha_beta_pruning=False,
                                     transposition_table=False)

        N_STEPS = 10

        for _ in range(0, N_STEPS):
            m_tt = strat_tt.select_move(game, game.player_turn)

            h_tt = strat_tt.heuristic.value(game, game.player_turn)
            h_no_tt = strat_no_tt.heuristic.value(game, game.player_turn)

            self.assertAlmostEqual(h_tt, h_no_tt, 2)

            game.apply_move_sequence(m_tt)
