from copy import deepcopy
import random

from chinese_checkers.cc_game import CCGame


class CCZobristHash():
    """
    https://en.wikipedia.org/wiki/Zobrist_hashing
    """

    def __init__(self, game: CCGame):
        self.table_1 = deepcopy(game.board)
        self.table_2 = deepcopy(game.board)
        for i in range(0, len(self.table_1)):
            for j in range(0, len(self.table_1[i])):
                self.table_1[i][j] = random.getrandbits(128)
                self.table_2[i][j] = random.getrandbits(128)

    def get_hash(self, game: CCGame):
        hash_ = 0
        for i in range(0, len(game.board)):
            for j in range(0, len(game.board[i])):
                if game.board[i][j] != 0:
                    hash_ = hash_ ^ (
                        self.table_1[i][j] if game.board[i][j] else
                        self.table_2[i][j]
                    )
        return hash_
