import random
import time

from chinese_checkers.cc_game import CCGame
from chinese_checkers.greedy_strategy import GreedyStrategy


if __name__ == "__main__":
    random.seed(1)

    game = CCGame(width=6, player_row_spawn=3)
    strategy_1 = GreedyStrategy(steps=0)
    strategy_2 = GreedyStrategy(steps=0)

    start = time.time()

    player_turn = 2
    game.rotate_turn()

    while(game.state() == 0):
        print(f'Turn: {player_turn}')
        assert game.player_turn == player_turn
        game.pretty_print_board()

        strategy = strategy_1 if player_turn == 1 else strategy_2
        move = strategy.select_move(game, player_turn)

        print(f'Move sequence: {move}')
        game.apply_move_sequence(move)

        if game.player_turn == player_turn:
            game.rotate_turn()
        player_turn = game.player_turn

        print('..........................')

    game.pretty_print_board()
    print(f'PLAYER {game.state()} WINS')
    end = time.time()
    print(end - start)
