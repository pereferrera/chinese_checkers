from chinese_checkers.cc_reasoner import CCReasoner
from chinese_checkers.cc_game import CCGame
from chinese_checkers.cc_heuristics import combined_vertical_advance


class GreedyStrategy(CCReasoner):

    def __init__(self, steps=1, alpha_beta_pruning=True,
                 heuristic=combined_vertical_advance):
        self.steps = steps
        self.alpha_beta_pruning = alpha_beta_pruning
        self.heuristic = heuristic

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
        moves = self.available_moves(game, player)
        if game.player_turn != player:
            raise AssertionError("""
                Player turn hasn't been rotated properly - this is likely
                a software bug
            """)

        best_move = None
        maximizing = depth % 2 == 0
        best_score = -100000 if maximizing else 100000

        for move in moves:
            if not best_move:
                best_move = move

            game.apply_move_sequence(move)
            if game.player_turn == player:
                # if we have been jumping, finish the movement
                game.rotate_turn()

            # check if game has already ended
            if game.state() == 1:
                # player 1 wins
                curr_score = 100000 if player == 1 else -100000
                if not maximizing:
                    curr_score = -curr_score
            elif game.state() == 2:
                # player 2 wins
                curr_score = -100000 if player == 1 else 100000
                if not maximizing:
                    curr_score = -curr_score
            else:
                if depth == self.steps * 2:  # maximizing
                    if player == 1:
                        # approximate the score of the game by
                        # subtracting heuristics
                        curr_score = (
                            self.heuristic(game, 1) -
                            self.heuristic(game, 2)
                        )
                    else:
                        curr_score = (
                            self.heuristic(game, 2) -
                            self.heuristic(game, 1)
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

        return (best_move, best_score)

    def select_move(self, game: CCGame, player: int):
        move, _ = self._select_move(game, player, 0, -100000, 100000)
        return move
