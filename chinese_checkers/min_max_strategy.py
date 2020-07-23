from typing import Tuple, Dict, Optional
from queue import PriorityQueue


from chinese_checkers.game import CCGame
from chinese_checkers.only_max_strategy import OnlyMaxStrategy
from chinese_checkers.heuristic import CCHeuristic
from chinese_checkers.heuristics import CombinedHeuristic
from chinese_checkers.helpers import CCZobristHash
from chinese_checkers.move import CCMove, PrioritizedCCMove
from chinese_checkers.strategy import CCStrategy


class MinMaxStrategy(CCStrategy):
    """
    Choose the best movement based on building a Min/Max tree
    Optionally apply alpha-beta pruning and/or transposition table lookup
    """

    def __init__(self, steps: int=1,
                 alpha_beta_pruning: bool=True,
                 pre_sort_moves: bool=False,
                 extra_prunning: bool=False,
                 transposition_table: bool=False,
                 heuristic: CCHeuristic=CombinedHeuristic()):
        self.steps = steps
        self.alpha_beta_pruning = alpha_beta_pruning
        self.pre_sort_moves = pre_sort_moves
        if self.pre_sort_moves and not self.alpha_beta_pruning:
            raise ValueError("""
                Invalid config: pre-sort moves without alpha beta pruning""")
        self.heuristic = heuristic
        # TODO must be better named and/or documented
        self.extra_prunning = extra_prunning
        self.transposition_table = transposition_table
        self.hasher: Optional[CCZobristHash] = None

    def _use_only_max(self, game: CCGame):
        """Returns True if the strategy can avoid running a MinMax and
        instead a pure maximization strategy can be used, at this point of
        the game. This happens at the beginning and end of the game, when
        teams are separated enough from each other."""
        p1_max = 0
        p1_min = len(game.board)
        p2_min = len(game.board)
        p2_max = 0

        for row in range(0, len(game.board)):
            for column in range(0, len(game.board[row])):
                if game.board[row][column] == 1:
                    p1_max = max(p1_max, row)
                    p1_min = min(p1_min, row)
                elif game.board[row][column] == 2:
                    p2_max = max(p2_max, row)
                    p2_min = min(p2_min, row)

        if (p2_min - p1_max - 1) > (self.steps + 1):
            # beginning of game, no use in doing min-max
            return True
        elif (p1_min - p2_max - 1) > (self.steps + 1):
            # end of game, no use in doing min-max
            return True
        return False

    def _select_move(self,
                     game: CCGame,
                     player: int,
                     depth: int,
                     alpha: float,
                     beta: float) -> Tuple[CCMove, float]:
        """
        Returns: tuple
            - position 0: best movem that can be done by the player
                at this level.
            - position 1: best heuristic value that can be achieved at this
                level if following best move.
                Heuristic is negative for player 2 and position for player 1.
        """
        if self.hasher:
            # transposition table business logic
            position_hash = self.hasher.get_hash(game)
            tt = (
                self.transposition_table_1 if player == 1 else
                self.transposition_table_2
            )
            best_move, best_score, cached_depth = (
                tt.get(position_hash, (None, -100000.0, -1))
            )
            if best_move and cached_depth == depth:
                return (best_move, best_score)

        moves = self.available_moves(game, player)
        if game.player_turn != player:
            raise AssertionError("""
                Player turn hasn't been rotated properly - this is likely
                a software bug
            """)

        moves_queue = PriorityQueue()

        for move in moves:
            priority = 1
            positions = move.board_positions
            if self.pre_sort_moves:
                advance = (
                    positions[-1][0] - positions[0][0] if player == 1 else
                    positions[0][0] - positions[-1][0]
                )

                if(self.extra_prunning
                   and advance <= 0
                   and depth >= 3):
                    # prune movements down the tree which don't bring any
                    # extra advance
                    continue

                # otherwise sort movements by vertical advance to maximize
                # alpha-beta pruning
                priority = -advance
            moves_queue.put(PrioritizedCCMove(priority, move))

        best_move = None
        maximizing = depth % 2 == 0
        best_score = -100000.0 if maximizing else 100000.0

        while not moves_queue.empty():
            move = moves_queue.get().move
            if not best_move:
                best_move = move

            game.apply_move_sequence(move)

            # check if game has already ended
            if game.state() == 1:
                # player 1 wins
                # prefer winning in as few steps as possible
                curr_score = (
                    100000 / (depth + 1) if player == 1 else -100000
                )
                if not maximizing:
                    curr_score = -curr_score
            elif game.state() == 2:
                # player 2 wins
                # prefer winning in as few steps as possible
                curr_score = (
                    -100000 if player == 1 else 100000 / (depth + 1)
                )
                if not maximizing:
                    curr_score = -curr_score
            else:
                if depth == self.steps * 2:  # maximizing
                        # approximate the score of the game by
                        # subtracting heuristics
                    curr_score = (
                        self.heuristic.value(game, player) -
                        self.heuristic.value(game, 2 if player == 1 else 1)
                    )
                else:
                    curr_score = self._select_move(game,
                                                   2 if player == 1 else 1,
                                                   depth + 1,
                                                   alpha, beta)[1]

            # keep the best move that can be done at this level
            if((maximizing and curr_score > best_score) or
               (not maximizing and curr_score < best_score)):
                best_score = curr_score
                best_move = move

            # undo movement
            if game.player_turn != player:
                game.rotate_turn()
            for _ in range(0, len(move.directions)):
                game.undo_last_move()

            # perform alpha-beta pruning
            if self.alpha_beta_pruning:
                if maximizing:
                    alpha = max(alpha, best_score)
                else:
                    beta = min(beta, best_score)
                if beta <= alpha:
                    # alpha/beta pruning
                    break

        if best_move:
            if self.hasher:
                # save into transposition table
                tt[position_hash] = (best_move, best_score, depth)
            return (best_move, best_score)
        else:
            raise AssertionError("""
                No possible movements available, this must be a software bug
            """)

    def select_move(self, game: CCGame, player: int) -> CCMove:
        if self.transposition_table:
            # initialize transposition tables on every turn
            self.transposition_table_1: Dict[int, Tuple[CCMove, float, int]] =\
                {}
            self.transposition_table_2: Dict[int, Tuple[CCMove, float, int]] =\
                {}
            if not self.hasher:
                # initialize hasher (only once for each game instance)
                self.hasher = CCZobristHash(game)
        if self._use_only_max(game):
            only_max = OnlyMaxStrategy(
                player,
                self.steps,
                transposition_table=self.transposition_table,
                heuristic=self.heuristic)
            # reuse hasher instance
            only_max.hasher = self.hasher
            move = only_max.select_move(game, player)
        else:
            move, _ = self._select_move(game, player, 0, -100000.0, 100000.0)
        return move
