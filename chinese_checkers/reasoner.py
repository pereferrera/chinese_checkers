from typing import List

from chinese_checkers.game import CCGame
from chinese_checkers.movement import CCMovement
from chinese_checkers.move import CCMove


class CCReasoner():
    """
    Base class for implementing players. Contains primitives like
    calculating the possible moves given the current board.
    """

    @staticmethod
    def _available_moves(game: CCGame,
                         row: int,
                         column: int,
                         player: int,
                         previous_moves: list = [],
                         previous_positions: list = []) -> List[CCMove]:
        """
        Returns a dict a list of movements that the player
        can make, considering the piece found at 'row' and 'column'
        """
        moves: List[CCMove] = []
        jumping = game.player_can_only_jump

        def undo_movement():
            if game.player_turn != player:
                game.rotate_turn()
            game.undo_last_move()
            if not jumping and game.player_can_only_jump:
                # reset jumping state
                game.player_can_only_jump = False

        for movement in CCMovement:
            if game.can_move(row, column, movement):
                turn = game.move(row, column, movement)
                if (game.moved_to_row[-1],
                        game.moved_to_column[-1]) in previous_positions:
                    # we already passed through this state, avoid
                    # infinite recursion
                    undo_movement()
                    continue
                previous_positions.append((game.moved_to_row[-1],
                                           game.moved_to_column[-1]))
                previous_moves.append(movement)
                moves.append(CCMove([*previous_positions], [*previous_moves]))
                if turn == player:
                    # turn hasn't rotated -> current piece can still jump more
                    moves += (CCReasoner._available_moves(
                        game,
                        game.moved_to_row[-1],
                        game.moved_to_column[-1],
                        player,
                        previous_moves,
                        previous_positions))
                previous_positions.pop()
                previous_moves.pop()
                undo_movement()

        return moves

    @staticmethod
    def available_moves(game: CCGame, player: int) -> List[CCMove]:
        """
        Returns a list of movements that the player can make.
        The value sequence is made of pairs in which:
        - position 0: contains the list of board positions that the piece
            can traverse
        - position 1: contains the list of CCMovement directions that the
            piece can apply in order to follow the traversed path
        """
        if player != game.player_turn:
            return []

        moves: List[CCMove] = []

        for row in range(0, len(game.board)):
            for column in range(0, len(game.board[row])):
                # if there is a piece from this player at this position,
                # check what can we do with it
                if game.board[row][column] == player:
                    moves += CCReasoner._available_moves(game,
                                                         row,
                                                         column,
                                                         player,
                                                         [],
                                                         [(row, column)])

        return moves
