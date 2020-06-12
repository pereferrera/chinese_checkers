"""
1 versus 1 chinese checkers
Representes the board and the state of the game
Encodes the rules i.e. it can be used to derive the allowed movements
and state transitions.
"""
from chinese_checkers.cc_movement import CCMovement


class CCGame:

    # minimum width of longest row of the board
    MIN_BOARD_WIDTH = 5
    # how many rows do each players' pieces spawn initially
    PLAYER_ROW_SPAWN = 3

    def __init__(self, width: int=5):
        if width < 5:
            raise ValueError("Longest board row length can't be less than "
                             f"{self.MIN_BOARD_WIDTH}")
        # player 1
        self.board = [[1] * i for i in range(1, self.PLAYER_ROW_SPAWN + 1)]
        # rest of board (empty)
        self.board += [[0] * i for i in range(self.PLAYER_ROW_SPAWN + 1,
                                              width + 1)]
        self.board += [[0] * i for i in reversed(range(self.PLAYER_ROW_SPAWN + 1,
                                                       width))]
        # player 2
        self.board += [[2] * i for i in reversed(
            range(1, self.PLAYER_ROW_SPAWN + 1))]

        # player 1 always starts
        self.player_turn = 1

    def within_bounds(self, row: int, column: int):
        """
        True if the position is allowed on this board, False otherwise
        """
        return not(
            (row < 0 or row >= len(self.board)) or
            (column < 0 or column >= len(self.board[row]))
        )

    def _dest_position(self, row: int, column: int, movement: CCMovement):
        """
        Calculates the destination position of a movement from a starting
        position. Returns a tuple (dest_row, dest_column).
        The calculated position might be out of bounds.
        """
        dest_row = row
        dest_column = column

        if(movement in [CCMovement.LN, CCMovement.RN]):
            dest_row -= 1
        elif(movement in [CCMovement.LS, CCMovement.RS]):
            dest_row += 1
        if(movement in [CCMovement.L]):
            dest_column -= 1
        elif(movement in [CCMovement.R, CCMovement.RN,
                          CCMovement.RS]):
            dest_column += 1

        return (dest_row, dest_column)

    def rotate_turn(self):
        """TODO Only allowed if current player actually moved something"""
        self.player_turn = 2 if self.player_turn == 1 else 1

    def _dest_jump_position(self, row: int, column: int, movement: CCMovement):
        dest_row, dest_column = self._dest_position(row, column, movement)
        return self._dest_position(dest_row, dest_column, movement)

    def _can_jump(self, row: int, column: int, movement: CCMovement):
        dest_row_jump, dest_column_jump = (
            self._dest_jump_position(row, column, movement)
        )
        if(not self.within_bounds(dest_row_jump, dest_column_jump)
           or self.board[dest_row_jump][dest_column_jump] != 0):
            return False
        return True

    def move(self, row: int, column: int, movement: CCMovement):
        """
        Given a starting position, move the piece according to an 
        executed direction. If there is a piece traversing the direction 
        of the movement, jump it. If the movement is invalid, a ValueException
        is raised.
        
        The board is modified and the player turned is rotated. In case
        the player has jumped a piece, and in case that more jumps are possible,
        the player turn is not rotated, indicating that the current player
        can still perform more moves.
        
        Returns the next player's turn.
        """
        if not self.within_bounds(row, column):
            raise ValueError('Out of bounds position in the board')
        if self.board[row][column] != self.player_turn:
            raise ValueError(f"It is player's {self.player_turn} turn.")

        dest_row, dest_column = self._dest_position(row, column, movement)

        if not self.within_bounds(row, column):
            raise ValueError('Movement ends in an out-of-bounds position')

        if self.board[dest_row][dest_column] != 0:
            # only allowed if we can jump this piece
            if self._can_jump(row, column, movement):
                # else movement is valid and we jumped a piece
                dest_row_jump, dest_column_jump = (
                    self._dest_jump_position(row, column, movement)
                )
                self.board[dest_row_jump][dest_column_jump] = (
                    self.board[row][column]
                )
                self.board[row][column] = 0
                # check if more jumps are still possible
                # if so, we exit and not rotate the turn, giving the current
                # player the possibility to still jump more
                for possible_move in CCMovement:
                    if self._can_jump(dest_row_jump,
                                      dest_column_jump,
                                      possible_move):
                        return self.player_turn
            else:
                raise ValueError("Can't jump over this piece")
        else:
            # destination is empty, movement is valid
            self.board[dest_row][dest_column] = self.board[row][column]
            self.board[row][column] = 0
        # rotate turn
        self.rotate_turn()
        return self.player_turn
