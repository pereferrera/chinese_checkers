import unittest

from chinese_checkers import cc_game
from chinese_checkers.cc_movement import CCMovement

TEST_BOARD = [[1],
              [1, 1],
              [1, 1, 1],
              [0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0],
              [2, 2, 2],
              [2, 2],
              [2]]


class TestCCGame(unittest.TestCase):

        def test_board(self):
            game = cc_game.CCGame(width=5)
            self.assertEqual(game.board,
                             TEST_BOARD)

        def test_allowed_move_no_jump_ls(self):
            game = cc_game.CCGame(width=5)
            self.assertEqual(1, game.board[2][0])
            game.move(2, 0, CCMovement.LS)
            self.assertEqual(0, game.board[2][0])
            self.assertEqual(1, game.board[3][0])

        def test_allowed_move_no_jump_rs(self):
            game = cc_game.CCGame(width=5)
            self.assertEqual(1, game.board[2][0])
            game.move(2, 0, CCMovement.RS)
            self.assertEqual(0, game.board[2][0])
            self.assertEqual(1, game.board[3][1])

        def test_allowed_move_no_jump_ln(self):
            game = cc_game.CCGame(width=5)
            game.rotate_turn()
            self.assertEqual(2, game.board[6][0])
            game.move(6, 0, CCMovement.LN)
            self.assertEqual(0, game.board[6][0])
            self.assertEqual(2, game.board[5][0])

        def test_allowed_move_no_jump_rn(self):
            game = cc_game.CCGame(width=5)
            game.rotate_turn()
            self.assertEqual(2, game.board[6][0])
            game.move(6, 0, CCMovement.RN)
            self.assertEqual(0, game.board[6][0])
            self.assertEqual(2, game.board[5][1])

        def test_allowed_move_no_jump_r(self):
            game = cc_game.CCGame(width=5)
            game.move(2, 0, CCMovement.RS)
            game.rotate_turn()
            game.move(3, 1, CCMovement.L)
            self.assertEqual(0, game.board[2][0])
            self.assertEqual(1, game.board[3][0])

        def test_allowed_move_no_jump_l(self):
            game = cc_game.CCGame(width=5)
            game.move(2, 0, CCMovement.LS)
            game.rotate_turn()
            game.move(3, 0, CCMovement.R)
            self.assertEqual(0, game.board[2][0])

        @unittest.expectedFailure
        def test_invalid_move_simple(self):
            game = cc_game.CCGame(width=5)
            game.move(0, 0, CCMovement.RN)

        def test_jump(self):
            game = cc_game.CCGame(width=5)
            game.move(1, 0, CCMovement.LS)  # jumps over piece at 2,0
            self.assertEqual(0, game.board[1][0])
            self.assertEqual(1, game.board[3][0])

        @unittest.expectedFailure
        def test_jump_invalid(self):
            game = cc_game.CCGame(width=5)
            game.move(0, 0, CCMovement.LS)
