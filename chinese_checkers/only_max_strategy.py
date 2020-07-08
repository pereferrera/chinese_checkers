from chinese_checkers.cc_reasoner import CCReasoner
from chinese_checkers.cc_game import CCGame
from chinese_checkers.cc_heuristic import CCHeuristic
from chinese_checkers.cc_heuristics import CombinedHeuristic
from chinese_checkers.helpers import CCZobristHash


class OnlyMaxStrategy(CCReasoner):
    """
    This Strategy is used internally by MinMaxStrategy, it is not supposed
    to be used standalone.
    """

    def __init__(self,
                 player: int,
                 steps: int=1,
                 hasher: CCZobristHash=None,
                 heuristic: CCHeuristic=CombinedHeuristic()):
        self.player = player
        self.steps = steps
        self.heuristic = heuristic
        # to use transposition tables
        self.hasher = hasher
        if self.hasher:
            self.transposition_table = {}

    def _select_move(self,
                     game: CCGame,
                     depth: int):
        """
        Returns: tuple
            - position 0: best movement that can be done by the player
                at this level. Movement is a tuple as per the values in
                #CCReasoner.available_moves()
            - position 1: best heuristic value that can be achieved at this
                level if following best move.
        """
        best_move, best_score = (None, -100000)
        if self.hasher:
            # transposition table business logic
            position_hash = self.hasher.get_hash(game)
            best_move, best_score, cached_depth = self.transposition_table.get(
                position_hash,
                (None, -100000, -1))

            if best_move and cached_depth == depth:
                return (best_move, best_score)

        moves = self.available_moves(game, self.player)
        if game.player_turn != self.player:
            raise AssertionError("""
                Player turn hasn't been rotated properly - this is likely
                a software bug
            """)

        for move in moves:
            if not best_move:
                best_move = move

            game.apply_move_sequence(move)
            # doesn't matter what the other does
            game.rotate_turn()

            # check if game has already ended
            if game.state() == 1:
                # player 1 wins
                # prefer winning in as few steps as possible
                curr_score = (
                    100000 / (depth + 1) if self.player == 1 else -100000
                )
            elif game.state() == 2:
                # player 2 wins
                # prefer winning in as few steps as possible
                curr_score = (
                    -100000 if self.player == 1 else 100000 / (depth + 1)
                )
            else:
                if depth == self.steps:
                    curr_score = self.heuristic.value(game, self.player)
                else:
                    curr_score = self._select_move(game,
                                                   depth + 1)[1]

            # keep the best move that can be done at this level
            if(curr_score > best_score):
                best_score = curr_score
                best_move = move
            elif(curr_score == best_score):
                if len(move[0]) < len(best_move[0]):
                    # prefer shorter moves
                    best_move = move

            # undo movement
            for _ in range(0, len(move[1])):
                game.undo_last_move()

        if self.hasher:
            # save into transposition table
            self.transposition_table[position_hash] = (best_move, best_score,
                                                       depth)
        return (best_move, best_score)

    def select_move(self, game: CCGame):
        move, _ = self._select_move(game, 0)
        return move
