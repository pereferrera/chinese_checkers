import unittest
from chinese_checkers.helpers import CCZobristHash
from chinese_checkers.cc_game import CCGame
from chinese_checkers.cc_movement import CCMovement

class TestCCGame(unittest.TestCase):

    def test_zobrist_hashing(self):
        game = CCGame(width=5)

        hasher = CCZobristHash(game)

        game_2 = CCGame(width=5)
        
        self.assertEqual(hasher.get_hash(game), 
                         hasher.get_hash(game_2))

        game.move(2, 0, CCMovement.LS)
        
        self.assertFalse(hasher.get_hash(game) == 
                         hasher.get_hash(game_2))
