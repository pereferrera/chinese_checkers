from copy import deepcopy

from chinese_checkers.cc_game import CCGame
from chinese_checkers.cc_movement import CCMovement
from chinese_checkers.exceptions import InvalidMoveException


class CCReasoner():

    @staticmethod
    def _available_moves(game: CCGame,
                         row: int,
                         column: int,
                         player: int,
                         previous_moves: list=[],
                         previous_positions: list=[]):
        """
        Returns a dict where the keys are the CCGame state after a move
        and the values are the sequence (list) of movements that the player
        can make to end up in that state, considering the piece found at
        'row' and 'column'
        """
        moves = {}

        for movement in CCMovement:
            m_game = deepcopy(game)
            try:
                turn = m_game.move(row, column, movement)
                if (m_game.moved_to_row,
                        m_game.moved_to_column) in previous_positions:
                    # we already passed through this state, avoid
                    # infinite recursion
                    continue
                current_positions = deepcopy(previous_positions)
                current_positions.append((m_game.moved_to_row,
                                          m_game.moved_to_column))
                current_moves = deepcopy(previous_moves)
                current_moves.append(movement)
                moves[m_game] = (current_positions, current_moves)
                if turn == player:
                    # turn hasn't rotated -> current piece can still jump more
                    moves.update(CCReasoner._available_moves(
                        m_game,
                        m_game.moved_to_row,
                        m_game.moved_to_column,
                        player,
                        current_moves,
                        current_positions))
            except InvalidMoveException:
                # move not allowed, skip
                pass

        return moves

    @staticmethod
    def available_moves(game: CCGame, player: int):
        """
        Returns a dict where the keys are the CCGame state after a move
        and the values are the sequence (list) of movements that the player
        can make to end up in that state.
        The value sequence is made of pairs in which:
        - position 0: contains the list of board positions that the piece
            can traverse
        - position 1: contains the list of CCMovement directions that the 
            piece can apply in order to follow the traversed path
        """
        if player != game.player_turn:
            return {}

        moves = {}

        for row in range(0, len(game.board)):
            for column in range(0, len(game.board[row])):
                # if there is a piece from this player at this position,
                # check what can we do with it
                if game.board[row][column] == player:
                    moves.update(CCReasoner._available_moves(game,
                                                             row,
                                                             column,
                                                             player,
                                                             [],
                                                             [(row, column)]))

        return moves
