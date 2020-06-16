import random

from chinese_checkers.cc_reasoner import CCReasoner
from chinese_checkers.cc_game import CCGame


class RandomStrategy(CCReasoner):

    def select_move(self, game: CCGame, player: int):
        """
        Returns: tuple
            best movement that can be done by the player
            at this level. Movement is a tuple as per the values in 
            #CCReasoner.available_moves() 
        """
        moves = self.available_moves(game, player)
        return random.choice(list(moves.values()))
