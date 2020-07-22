from chinese_checkers.heuristic import CCHeuristic
from chinese_checkers.game import CCGame


class CombinedHeuristic(CCHeuristic):

    def __init__(self, weights: list=[0.01,
                                      0.44,
                                      0.55]):
        self.weights = weights

    def value(self, game: CCGame, player: int):
        # rough normalization to combine different heuristics
        return (
            self.weights[0] * InvSquaredSumCenterLine().value(game, player) +
            self.weights[1] * CombinedVerticalAdvance().value(game, player) +
            self.weights[2] * InvSquaredSumDestCorner().value(game, player)
        )


class CombinedVerticalAdvance(CCHeuristic):

    def value(self, game: CCGame, player: int):
        """
        Returns:
        -------
        float
            The sum of vertical advance for all pieces of the passed player,
            as metric between 1 and 0
        """
        heigth = len(game.board)
        combined_va = 0
        pieces = 0
        for row in range(0, heigth):
            for column in range(0, len(game.board[row])):
                if game.board[row][column] == player:
                    pieces += 1
                    combined_va += (
                        row if player == 1 else (heigth - row - 1)
                    )
        return combined_va / (heigth * pieces)


class InvSquaredSumCenterLine(CCHeuristic):

    def value(self, game: CCGame, player: int):
        """
        Returns:
        -------
        float
            The inverse squared sum of the distances of all pieces
            from this player to the center line.
        """
        squared_sum = 0.0

        heigth = len(game.board)

        for row in range(0, heigth):
            center = (len(game.board[row]) / 2)
            for column in range(0, len(game.board[row])):
                if game.board[row][column] == player:
                    dist = abs(column - center)
                    squared_sum += (dist * dist)

        if squared_sum == 0:
            return 1.0
        return min(1.0, 1 / squared_sum)


class InvSquaredSumDestCorner(CCHeuristic):

    def value(self, game: CCGame, player: int):
        """
        Returns:
        -------
        float
            The inverse squared sum of the distances of all pieces
            from this player to its destiny corner (0,0) or (n,0).
            This is actually calculated as 1 - the inverse squared sum of
            distances to the origin such that the gain is bigger at the
            beginning and smaller as the pieces approach the destiny (to
            avoid trailing pieces).
        """
        squared_sum = 0

        heigth = len(game.board)
        dest_row = 0
        dest_column = 0

        if player == 2:
            dest_row = heigth - 1

        for row in range(0, heigth):
            for column in range(0, len(game.board[row])):
                if game.board[row][column] == player:
                    dist = max(abs(dest_row - row),
                               abs(dest_column - column))
                    squared_sum += (dist * dist)

        return 1 - min(1, 1 / squared_sum)
