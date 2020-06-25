from chinese_checkers.cc_reasoner import CCReasoner
from chinese_checkers.cc_game import CCGame
from chinese_checkers.cc_heuristics import combined_vertical_advance


class OnlyMaxStrategy(CCReasoner):

    def __init__(self,
                 player,
                 steps=1,
                 heuristic=combined_vertical_advance):
        self.player = player
        self.steps = steps
        self.heuristic = heuristic

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
        moves = self.available_moves(game, self.player)
        if game.player_turn != self.player:
            raise AssertionError("""
                Player turn hasn't been rotated properly - this is likely
                a software bug
            """)

        best_move = None
        best_score = -100000

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
                    100000/(depth + 1) if self.player == 1 else -100000
                )
            elif game.state() == 2:
                # player 2 wins
                # prefer winning in as few steps as possible
                curr_score = (
                    -100000 if self.player == 1 else 100000/(depth + 1)
                )
            else:
                if depth == self.steps:
                    curr_score = self.heuristic(game, self.player)
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

        return (best_move, best_score)

    def select_move(self, game: CCGame):
        move, _ = self._select_move(game, 0)
        return move
