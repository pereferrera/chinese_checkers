import unittest
from chinese_checkers.game import CCGame
from chinese_checkers.reasoner import CCReasoner
from chinese_checkers.movement import CCMovement
from chinese_checkers.move import CCMove


class TestCCReasoner(unittest.TestCase):

    def test_available_moves(self):
        game = CCGame(width=5)
        moves = CCReasoner.available_moves(game, 1)
        self.assertEqual(moves,
                         [CCMove([(1, 0), (3, 0)], [CCMovement.LS]),
                          CCMove([(1, 0), (3, 2)], [CCMovement.RS]),
                          CCMove([(1, 1), (3, 1)], [CCMovement.LS]),
                          CCMove([(1, 1), (3, 3)], [CCMovement.RS]),
                          CCMove([(2, 0), (3, 0)], [CCMovement.LS]),
                          CCMove([(2, 0), (3, 1)], [CCMovement.RS]),
                          CCMove([(2, 1), (3, 1)], [CCMovement.LS]),
                          CCMove([(2, 1), (3, 2)], [CCMovement.RS]),
                          CCMove([(2, 2), (3, 2)], [CCMovement.LS]),
                          CCMove([(2, 2), (3, 3)], [CCMovement.RS])])

    def test_available_moves_player_2(self):
        game = CCGame(width=5)
        moves_1 = CCReasoner.available_moves(game, 1)
        game.rotate_turn()
        moves_2 = CCReasoner.available_moves(game, 2)
        self.assertEqual(len(moves_1), len(moves_2))

    def test_available_moves_depth_2(self):
        game = CCGame(width=5)
        game.move(2, 0, CCMovement.RS)
        game.rotate_turn()
        moves = CCReasoner.available_moves(game, 1)
        self.assertTrue(CCMove([(0, 0), (2, 0), (4, 2)],
                               [CCMovement.LS, CCMovement.RS]) in moves)
        self.assertTrue(CCMove([(1, 0), (3, 2), (3, 0)],
                               [CCMovement.RS, CCMovement.L]) in moves)
        self.assertTrue(CCMove([(2, 2), (2, 0), (4, 2)],
                               [CCMovement.L, CCMovement.RS]) in moves)
