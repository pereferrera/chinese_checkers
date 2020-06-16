import unittest
from chinese_checkers.cc_game import CCGame
from chinese_checkers.greedy_strategy import GreedyStrategy
from chinese_checkers.cc_reasoner import CCReasoner

from constants import TEST_BOARD_STRATEGY


# limit the depth of the tree for testing pu rposes
def patched_available_moves(game, player):
    moves = CCReasoner.available_moves(game, player)
    if len(moves) > 2:
        return {k: moves[k] for k in list(moves.keys())[-2:]}


class TestCCReasoner(unittest.TestCase):

    def test_greedy_strategy(self):
        game = CCGame(width=5, player_row_spawn=2)
        game.board = TEST_BOARD_STRATEGY
        strategy = GreedyStrategy(alpha_beta_pruning=False)

        strategy.available_moves = patched_available_moves
        _, score = strategy._select_move(game, 1, 0, -100000, 100000)

        self.assertEqual(1, score)