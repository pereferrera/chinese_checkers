from typing import Optional, Dict, Tuple

from chinese_checkers.game import CCGame
from chinese_checkers.heuristic.heuristic import CCHeuristic
from chinese_checkers.heuristic.heuristics import CombinedHeuristic
from chinese_checkers.helpers import CCZobristHash
from chinese_checkers.move import CCMove
from chinese_checkers.strategy.strategy import CCStrategy


class OnlyMaxStrategy(CCStrategy):
    """
    Strategy that only considers the sequence of movements of the player that
    is to move. This strategy can be used in situations where the movements of
    the opponent do not influence the current choice. Therefore it is used
    internally by MinMaxStrategy
    """

    def __init__(self,
                 player: int,
                 steps: int = 1,
                 transposition_table: bool = False,
                 heuristic: CCHeuristic = CombinedHeuristic()):
        self.player = player
        self.steps = steps
        self.heuristic = heuristic
        self.use_transposition_table = transposition_table
        self.hasher: Optional[CCZobristHash] = None

    def _select_move(self,
                     game: CCGame,
                     depth: int) -> Tuple[CCMove, float]:
        """
        Returns: tuple
            - position 0: best movet that can be done by the player
                at this level.
            - position 1: best heuristic value that can be achieved at this
                level if following best move.
        """
        best_move, best_score = (None, -100000.0)
        if self.use_transposition_table and self.hasher:
            # transposition table business logic
            position_hash = self.hasher.get_hash(game)
            best_move, best_score, cached_depth = self.transposition_table.get(
                position_hash,
                (None, -100000.0, -1))

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

            # undo movement
            for _ in range(0, len(move.directions)):
                game.undo_last_move()

        if best_move:
            if self.hasher:
                # save into transposition table
                self.transposition_table[position_hash] = (
                    best_move, best_score, depth
                )
            return (best_move, best_score)
        else:
            raise AssertionError("""
                No possible movements available, this must be a software bug
            """)

    def select_move(self, game: CCGame, _: int) -> CCMove:
        if self.use_transposition_table:
            self.transposition_table: Dict[int, Tuple[CCMove, float, int]] = {}
            if not self.hasher:
                # initialize hasher (only once for each game instance)
                self.hasher = CCZobristHash(game)
        move, __ = self._select_move(game, 0)
        return move
