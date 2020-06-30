from queue import PriorityQueue


from chinese_checkers.cc_reasoner import CCReasoner
from chinese_checkers.cc_game import CCGame
from chinese_checkers.only_max_strategy import OnlyMaxStrategy
from chinese_checkers.cc_heuristic import CCHeuristic
from chinese_checkers.cc_heuristics import CombinedHeuristic


class MinMaxStrategy(CCReasoner):

    def __init__(self, steps: int=1, alpha_beta_pruning: bool=True,
                 pre_sort_moves: bool=False,
                 heuristic: CCHeuristic=CombinedHeuristic()):
        self.steps = steps
        self.alpha_beta_pruning = alpha_beta_pruning
        self.pre_sort_moves = pre_sort_moves
        if self.pre_sort_moves and not self.alpha_beta_pruning:
            raise ValueError("""
                Invalid config: pre-sort moves without alpha beta pruning""")
        self.heuristic = heuristic
        self.hasher = None

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
                     alpha: int,
                     beta: int):
        """
        Returns: tuple
            - position 0: best movement that can be done by the player
                at this level. Movement is a tuple as per the values in 
                #CCReasoner.available_moves() 
            - position 1: best heuristic value that can be achieved at this
                level if following best move.
                Heuristic is negative for player 2 and position for player 1.
        """
        # TODO Some DRY here, move common code
#        if self.hasher:
#            position_hash = self.hasher.get_hash(game)
#            tt = (
#                self.transposition_table_1 if player == 1 else
#                self.transposition_table_2
#            )
#            best_move, best_score, cached_depth = (
#                tt.get(position_hash, (None, -100000, -1))
#            )
#            if best_move and cached_depth == depth:
#                self.hits += 1
#                return (best_move, best_score)
#            else:
#                self.misses += 1

        moves = self.available_moves(game, player)
        if game.player_turn != player:
            raise AssertionError("""
                Player turn hasn't been rotated properly - this is likely
                a software bug
            """)

        moves_queue = PriorityQueue()
        for move in moves:
            priority = 1
            if self.pre_sort_moves:
                game.apply_move_sequence(move)
                priority = -self.heuristic.value(game, player)
                # undo movement
                for _ in range(0, len(move[1])):
                    game.undo_last_move()
                game.rotate_turn()
            moves_queue.put((priority, move))

        best_move = None
        maximizing = depth % 2 == 0
        best_score = -100000 if maximizing else 100000

        while not moves_queue.empty():
            move = moves_queue.get()[1]
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
            elif(curr_score == best_score):
                if len(move[0]) < len(best_move[0]):
                    # prefer shorter moves
                    best_move = move

            # undo movement
            for _ in range(0, len(move[1])):
                game.undo_last_move()
            game.rotate_turn()

            # perform alpha-beta pruning
            if self.alpha_beta_pruning:
                if maximizing:
                    alpha = max(alpha, best_score)
                else:
                    beta = min(beta, best_score)
                if beta <= alpha:
                    # alpha/beta pruning
                    return (best_move, best_score)

#        if self.hasher:
#            tt[position_hash] = (best_move, best_score, depth)
        return (best_move, best_score)

    def select_move(self, game: CCGame, player: int):
        #        self.transposition_table_1 = {}
        #        self.transposition_table_2 = {}
        #        self.hasher = CCZobristHash(game)
        #        self.hits = 0
        #        self.misses = 0
        if self._use_only_max(game):
            only_max = OnlyMaxStrategy(player, self.steps,
                                       heuristic=self.heuristic)
            # TODO DRY, UGLY
#            only_max.transposition_table = {}
#            only_max.hasher = self.hasher
#            only_max.hits = 0
#            only_max.misses = 0
            move, _ = only_max._select_move(game, 0)
#            print(f'{only_max.hits} hits, {only_max.misses} misses')
        else:
            move, _ = self._select_move(game, player, 0, -100000, 100000)
#            print(f'{self.hits} hits, {self.misses} misses')
        return move
