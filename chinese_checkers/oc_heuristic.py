from chinese_checkers.game_visitor import GameVisitor
from chinese_checkers.cc_heuristic import CCHeuristic

"""
Stateful heuristic made with performance in mind.
Recalculate the heuristic value for every movement, avoiding repeated
calculations
"""


class OptimizedCombinedHeuristic(GameVisitor, CCHeuristic):

    def __init__(self, weights: list=[0.014289242,
                                      0.965580208,
                                      0.02013055]):
        self.weights = weights

    def _values_of(self, row: int, column: int, player: int):
        # vertical advance
        va = (row if player == 1 else (self.heigth - row - 1))

        # inverse squared distance to center line
        center = (len(self.board[row]) / 2)
        dist_center = abs(column - center)
        dist_center_sqrd = (dist_center * dist_center)

        # inverse squared distance to destination
        dest_row = self.heigth - 1
        if player == 2:
            dest_row = 0
        dist_dest = max(abs(dest_row - row), column)
        dist_dest_sqrd = dist_dest * dist_dest

        return [dist_center_sqrd, va, dist_dest_sqrd]

    def on_init_game(self, board: list):
        self.board = board
        self.heigth = len(board)
        self.pieces = 0

        self.value_1 = [0, 0, 0]
        self.value_2 = [0, 0, 0]

        for row in range(0, self.heigth):
            for column in range(0, len(board[row])):
                if board[row][column] == 1:
                    self.pieces += 1
                    plus = self._values_of(row, column, 1)
                    for i in range(0, 3):
                        self.value_1[i] = self.value_1[i] + plus[i]
                elif board[row][column] == 2:
                    plus = self._values_of(row, column, 2)
                    for i in range(0, 3):
                        self.value_2[i] = self.value_2[i] + plus[i]

    def on_move(self,
                from_row: int,
                from_column: int,
                dest_row: int,
                dest_column: int,
                player: int):
        """
        Update the heuristic values given that a player has moved a piece
        from point A to point B
        """
        minus = self._values_of(from_row, from_column, player)
        plus = self._values_of(dest_row, dest_column, player)

        if player == 1:
            for i in range(0, 3):
                self.value_1[i] = self.value_1[i] - minus[i] + plus[i]
        else:
            for i in range(0, 3):
                self.value_2[i] = self.value_2[i] - minus[i] + plus[i]

    def value(self, _, player: int):
        """
        Return the heuristic value between 0 and 1 with respect to the
        given player
        """
        vals = self.value_1 if player == 1 else self.value_2
        a = self.weights[0] * (1 if vals[0] == 0 else min(1, 1 / vals[0]))
        assert vals[1] < (self.heigth * self.pieces)
        b = self.weights[1] * (vals[1] / (self.heigth * self.pieces))
        c = self.weights[2] * (1 if vals[2] == 0 else min(1, 1 / vals[2]))
        return (a + b + c)
