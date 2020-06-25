import random
import time

from functools import partial
from scipy import stats

from chinese_checkers.cc_game import CCGame
from chinese_checkers.min_max_strategy import MinMaxStrategy
from chinese_checkers.pygame_gui import PygameGUI
from chinese_checkers.manual_player import ManualPlayer
from chinese_checkers.cc_heuristics import (
    combined_vertical_advance,
    inv_squared_sum_center_line,
    inv_squared_sum_dest_corner,
    combined_heuristic
)


if __name__ == "__main__":
    random.seed(1)

    game = CCGame(width=6, player_row_spawn=2)

#    manual_players = set([1])
    manual_players = set()

    ai_players = {
        1: MinMaxStrategy(steps=2, pre_sort_moves=True,
                          heuristic=partial(combined_heuristic,
                                            weights=[0.2660622210182407, 0.5110974627544762, 0.22284031622728318])),
        2: MinMaxStrategy(steps=2, pre_sort_moves=True,
                          heuristic=combined_heuristic)
    }

    start = time.time()

    player_turn = 2
    game.rotate_turn()

    turns = 0

    gui = PygameGUI(game)
    manual_player = ManualPlayer(gui)

    def print_metrics(player):
        print(f"""
        Player {player}:
            cva={combined_vertical_advance(game, player)} 
            iss_cl={inv_squared_sum_center_line(game, player)} 
            iss_dc={inv_squared_sum_dest_corner(game, player)}
        """)

    ai_players_perf = {
        1: [],
        2: []
    }

    while(game.state() == 0):
        print(f'Turn: {player_turn}')
        assert game.player_turn == player_turn
        gui.update()
        for player in [1, 2]:
            print_metrics(player)

        if player_turn not in manual_players:
            strategy = ai_players[player_turn]
            start = time.time()
            move = strategy.select_move(game, player_turn)
            end = time.time()
            ai_players_perf[player_turn].append(end - start)
            print(f'Move sequence: {move}')
            print(f'{stats.describe(ai_players_perf[player_turn])}')
            game.apply_move_sequence(move)
        else:
            print("It's manual's player turn!")
            manual_player.move(game, player_turn)
            if game.player_turn == player_turn:
                game.rotate_turn()

        player_turn = game.player_turn
        turns += 1

        print('..........................')

    print(f'PLAYER {game.state()} WINS after {turns} turns')
    end = time.time()
    print(end - start)
