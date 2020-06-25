"""
1 versus 1 chinese checkers
Representes the board and the state of the game
Encodes the rules i.e. it can be used to derive the allowed movements
and state transitions.
"""
from chinese_checkers.cc_movement import CCMovement
from chinese_checkers.exceptions import InvalidMoveException


class CCGame:

    NORTH_MOVEMENTS = set([CCMovement.LN, CCMovement.RN])
    SOUTH_MOVEMENTS = set([CCMovement.LS, CCMovement.RS])
    # minimum width of longest row of the board
    MIN_BOARD_WIDTH = 5

    def __init__(self, width: int=5, player_row_spawn=3):
        if width < 5:
            raise ValueError("Longest board row length can't be less than "
                             f"{self.MIN_BOARD_WIDTH}")
        if player_row_spawn > width - 2:
            raise ValueError(
                "Players' spawn can't be bigger than max width - 2")

        self.width = width
        self.player_row_spawn = player_row_spawn

        self.player_row_spawn = player_row_spawn
        # player 1
        self.board = [[1] * i for i in range(1, self.player_row_spawn + 1)]
        # rest of board (empty)
        self.board += [[0] * i for i in range(self.player_row_spawn + 1,
                                              width + 1)]
        self.board += [[0] * i for i in reversed(range(self.player_row_spawn + 1,
                                                       width))]
        # player 2
        self.board += [[2] * i for i in reversed(
            range(1, self.player_row_spawn + 1))]
        self.half_board = int(len(self.board) / 2)

        # player 1 always starts
        self.player_turn = 1
        self.player_can_only_jump = False

        self.moved_row = []
        self.moved_column = []
        self.moved_to_row = []
        self.moved_to_column = []

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

        if(movement in self.NORTH_MOVEMENTS):
            dest_row -= 1
        elif(movement in self.SOUTH_MOVEMENTS):
            dest_row += 1
        elif(movement == CCMovement.L):
            dest_column -= 1
        elif(movement == CCMovement.R):
            dest_column += 1

        if(movement == CCMovement.LN):
            if(dest_row < self.half_board):
                dest_column -= 1
        elif(movement == CCMovement.RS):
            if(dest_row <= self.half_board):
                dest_column += 1
        elif(movement == CCMovement.LS):
            if(dest_row > self.half_board):
                dest_column -= 1
        elif(movement == CCMovement.RN):
            if(dest_row >= self.half_board):
                dest_column += 1

        return (dest_row, dest_column)

    def rotate_turn(self):
        """
        Rotate the player's turn (i.e. a player is jumping and doesn't want
        to jump more). Returns the instance of the game.
        """
        self.player_turn = 2 if self.player_turn == 1 else 1
        self.player_can_only_jump = False
        return self

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

    def _do_move(self, from_row: int, from_column: int,
                 dest_row: int, dest_column: int):
        """Internal method which moves a piece and updates the board.
        Keeps track of what happened in internal variables."""
        self.board[dest_row][dest_column] = self.board[from_row][from_column]
        self.board[from_row][from_column] = 0

        # with these variables we could e.g. undo the last movement
        self.moved_row.append(from_row)
        self.moved_column.append(from_column)
        self.moved_to_row.append(dest_row)
        self.moved_to_column.append(dest_column)

    def undo_last_move(self):
        from_row = self.moved_to_row.pop()
        from_column = self.moved_to_column.pop()
        self.board[self.moved_row.pop()][self.moved_column.pop()] =\
            self.board[from_row][from_column]
        self.board[from_row][from_column] = 0

    def can_move(self, row: int, column: int, movement: CCMovement):
        """
        True if the player can move in this direction from the row and 
        column. Note: doesn't check if row, column are within bounds.
        """
        dest_row, dest_column = self._dest_position(row, column, movement)
        if not self.within_bounds(dest_row, dest_column):
            return False
        if self.board[dest_row][dest_column] != 0:
            # only allowed if we can jump this piece
            return self._can_jump(row, column, movement)
        else:
            return not self.player_can_only_jump

    def move(self, row: int, column: int, movement: CCMovement):
        """
        Given a starting position, move the piece according to an 
        executed direction. If there is a piece traversing the direction 
        of the movement, jump it. If the movement is invalid, a ValueException
        is raised.
        
        The board is modified and the player turned is rotated. In case
        the player has jumped a piece, and in case that more jumps are possible,
        the player turn is not rotated, indicating that the current player
        can still perform more moves. (Note: the game doesn't enforce yet
        that the next moves are from the same piece that was moved, but
        that should be ideally done). 
        
        Returns the next player's turn.
        
        @raise ValueError:
        @raise InvalidMoveException: 
        """
        if not self.within_bounds(row, column):
            raise ValueError('Out of bounds position in the board')
        if self.board[row][column] != self.player_turn:
            raise InvalidMoveException(
                f"It is player's {self.player_turn} turn.")

        dest_row, dest_column = self._dest_position(row, column, movement)

        if not self.within_bounds(dest_row, dest_column):
            raise InvalidMoveException(
                'Movement ends in an out-of-bounds position')

        if self.board[dest_row][dest_column] != 0:
            # only allowed if we can jump this piece
            if not self._can_jump(row, column, movement):
                raise InvalidMoveException("Can't jump over this piece")
            # else movement is valid and we jumped a piece
            dest_row_jump, dest_column_jump = (
                self._dest_jump_position(row, column, movement)
            )
            self._do_move(row, column, dest_row_jump, dest_column_jump)
            # check if more jumps are still possible
            # if so, we exit and not rotate the turn, giving the current
            # player the possibility to still jump more
            for possible_move in CCMovement:
                if self._can_jump(dest_row_jump,
                                  dest_column_jump,
                                  possible_move):
                    self.player_can_only_jump = True
                    return self.player_turn
        else:
            if self.player_can_only_jump:
                raise InvalidMoveException('Only more jumps are allowed')
            # destination is empty, movement is valid
            self._do_move(row, column, dest_row, dest_column)
        # rotate turn
        self.rotate_turn()
        return self.player_turn

    def apply_move_sequence(self, move_sequence):
        """Apply a sequence of possibly more than one move (e.g. by
        jumping). move_sequence is a tuple:
         - 0: list of positions the move sequence will traverse
         - 1: list of CCMovement directions the move sequence will perform
        This function automatically rotates the turn if jumps are performed
        (it is assumed no more movements from the same player will follow).
        """
        player = self.player_turn
        
        positions = move_sequence[0]
        directions = move_sequence[1]
        for i, direction in enumerate(directions):
            row, column = positions[i]
            self.move(row, column, direction)
    
        if self.player_turn == player:
            # if we have been jumping, finish the movement
            self.rotate_turn()

    def pretty_print_board(self):
        for i in range(0, len(self.board)):
            spacing = ' ' * (self.width - len(self.board[i]))
            str_row = ' '.join(map(str, self.board[i]))
            print(f'{spacing}{str_row}')

    def _player_1_wins(self):
        for i in range(0, self.player_row_spawn):
            if self.board[len(self.board) - i - 1] != [1] * (i + 1):
                return False
        return True

    def _player_2_wins(self):
        for i in range(0, self.player_row_spawn):
            if self.board[i] != [2] * (i + 1):
                return False
        return True

    def state(self):
        """
        Returns:
        --------
        int
            - 0: Game being played
            - 1: Player 1 wins
            - 2: Player 2 wins
        """
        return 2 if self._player_2_wins() else (
            1 if self._player_1_wins() else 0)

    def __repr__(self):
        return f"C({self.board} turn:{self.player_turn})"

    def __hash__(self):
        _hash = 2 ^ 16
        for row in range(0, len(self.board)):
            for column in range(0, len(self.board[row])):
                _hash ^= (row + 1) * (column + 1) * \
                    hash(self.board[row][column])
        return _hash ^ hash(self.player_turn)

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.board == other.board and
            self.player_turn == other.player_turn
        )
