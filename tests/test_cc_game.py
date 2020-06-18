import unittest

from chinese_checkers.cc_movement import CCMovement
from chinese_checkers.cc_game import CCGame

from constants import (
    TEST_BOARD, TEST_BOARD_PLAYER_1_WINS, TEST_BOARD_PLAYER_2_WINS,
    TEST_BOARD_PLAYER_1_DOES_NOT_WIN
)


class TestCCGame(unittest.TestCase):

        def test_board_equality_equals(self):
            game = CCGame(width=5)
            self.assertEqual(game.board,
                             TEST_BOARD)
            game_2 = CCGame(width=5)
            self.assertTrue(game == game_2)
            self.assertEqual(1, len(set([game, game_2])))
            
        def test_board_equality_non_equals(self):
            game_1 = CCGame(width=5)
            game_1.board[1][0] = 0
            game_1.board[3][0] = 1
            game_2 = CCGame(width=5)
            game_2.board[1][0] = 0
            game_2.board[3][2] = 1
            
            self.assertFalse(game_1 == game_2)
            self.assertEqual(2, len(set([game_1, game_2])))

        def test_state_playing(self):
            game = CCGame(width=5)
            self.assertEqual(0,
                             game.state())

        def test_state_player_1_wins(self):
            game = CCGame(width=5)
            game.board = TEST_BOARD_PLAYER_1_WINS
            self.assertEqual(1,
                             game.state())
            
        def test_state_player_1_does_not_win(self):
            game = CCGame(width=5)
            game.board = TEST_BOARD_PLAYER_1_DOES_NOT_WIN
            self.assertEqual(0,
                             game.state())

        def test_state_player_2_wins(self):
            game = CCGame(width=5)
            game.board = TEST_BOARD_PLAYER_2_WINS
            self.assertEqual(2,
                             game.state())

        def test_allowed_move_no_jump_ls_1(self):
            game = CCGame(width=5)
            self.assertEqual(1, game.board[2][0])
            game.move(2, 0, CCMovement.LS)
            self.assertEqual(0, game.board[2][0])
            self.assertEqual(1, game.board[3][0])

        def test_allowed_move_no_jump_ls_2(self):
            game = CCGame(width=5)
            game.board[3][2] = 1
            game.move(3, 2, CCMovement.LS)
            self.assertEqual(0, game.board[3][2])
            self.assertEqual(1, game.board[4][2])

        def test_allowed_move_no_jump_rs_1(self):
            game = CCGame(width=5)
            self.assertEqual(1, game.board[2][0])
            game.move(2, 0, CCMovement.RS)
            self.assertEqual(0, game.board[2][0])
            self.assertEqual(1, game.board[3][1])
    
        def test_allowed_move_no_jump_rs_2(self):
            game = CCGame(width=5)
            game.board[3][2] = 1
            game.move(3, 2, CCMovement.RS)
            self.assertEqual(0, game.board[3][2])
            self.assertEqual(1, game.board[4][3])

        def test_allowed_move_no_jump_ln_1(self):
            game = CCGame(width=5)
            game.rotate_turn()
            self.assertEqual(2, game.board[6][0])
            game.move(6, 0, CCMovement.LN)
            self.assertEqual(0, game.board[6][0])
            self.assertEqual(2, game.board[5][0])

        def test_allowed_move_no_jump_ln_2(self):
            game = CCGame(width=5)
            game.board[3][2] = 1
            game.board[2][1] = 0
            game.move(3, 2, CCMovement.LN)
            self.assertEqual(0, game.board[3][2])
            self.assertEqual(1, game.board[2][1])

        def test_allowed_move_no_jump_rn_1(self):
            game = CCGame(width=5)
            game.rotate_turn()
            self.assertEqual(2, game.board[6][0])
            game.move(6, 0, CCMovement.RN)
            self.assertEqual(0, game.board[6][0])
            self.assertEqual(2, game.board[5][1])

        def test_allowed_move_no_jump_rn_2(self):
            game = CCGame(width=5)
            game.board[3][2] = 1
            game.board[2][2] = 0
            game.move(3, 2, CCMovement.RN)
            self.assertEqual(0, game.board[3][2])
            self.assertEqual(1, game.board[2][2])

        def test_allowed_move_no_jump_r(self):
            game = CCGame(width=5)
            game.move(2, 0, CCMovement.RS)
            game.rotate_turn()
            game.move(3, 1, CCMovement.L)
            self.assertEqual(0, game.board[2][0])
            self.assertEqual(1, game.board[3][0])

        def test_allowed_move_no_jump_l(self):
            game = CCGame(width=5)
            game.move(2, 0, CCMovement.LS)
            game.rotate_turn()
            game.move(3, 0, CCMovement.R)
            self.assertEqual(0, game.board[2][0])

        @unittest.expectedFailure
        def test_invalid_move_simple(self):
            game = CCGame(width=5)
            game.move(0, 0, CCMovement.RN)

        def test_jump(self):
            game = CCGame(width=5)
            game.move(1, 0, CCMovement.LS)  # jumps over piece at 2,0
            self.assertEqual(0, game.board[1][0])
            self.assertEqual(1, game.board[3][0])

        @unittest.expectedFailure
        def test_jump_invalid(self):
            game = CCGame(width=5)
            game.move(0, 0, CCMovement.LS)
