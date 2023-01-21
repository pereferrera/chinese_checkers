import random
import time
import argparse
from typing import List, Dict

from scipy import stats

from chinese_checkers.game import CCGame
from chinese_checkers.strategy.min_max_strategy import MinMaxStrategy
from chinese_checkers.pygame_gui import PygameGUI
from chinese_checkers.manual_player import ManualPlayer
from chinese_checkers.heuristic.oc_heuristic import OptimizedCombinedHeuristic


"""
Entry point for playing interactively against the AI
"""


def play(board_size: int, player_row_span: int):
    random.seed(1)

    # (these weights were found running different experiments with the
    #  weight_search.py script)
    oc_heuristic = OptimizedCombinedHeuristic(weights=[0.13214166541392974,
                                                       0.5297777211424128,
                                                       0.290789326515336,
                                                       0.047291286928321644])

    game = CCGame(width=board_size,
                  player_row_span=player_row_span,
                  visitors=[oc_heuristic])

    manual_players = set([1])

    ai_players = {
        2: MinMaxStrategy(steps=1,
                          pre_sort_moves=True,
                          transposition_table=True,
                          heuristic=oc_heuristic)
    }

    start = time.time()

    player_turn = 1

    turns = 0

    gui = PygameGUI(game)
    manual_player = ManualPlayer(gui)

    ai_players_perf: Dict[int, List[float]] = {
        1: [],
        2: []
    }

    while(game.state() == 0):
        print(f'Turn: {player_turn}')
        assert game.player_turn == player_turn
        gui.update()

        if player_turn not in manual_players:
            strategy = ai_players[player_turn]
            start = time.time()
            move = strategy.select_move(game, player_turn)
            end = time.time()
            ai_players_perf[player_turn].append(end - start)
            print(f'Move sequence: {move}')
            print(f'Turn {turns}')
            print(('Performance: '
                   f'{stats.describe(ai_players_perf[player_turn])}'))
            print(f'Heuristic values: {oc_heuristic.value(game, 1)} - '
                  f'{oc_heuristic.value(game, 2)}')
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--board_size",
        type=int,
        default=9,
        help="Size of the board as total number of rows")
    parser.add_argument(
        "--player_row_span",
        type=int,
        default=4,
        help=("How many rows each player spans. These rows will be filled "
              "with pieces starting from the top or the bottom of th board "
              "e.g. 1 row=1 piece, 2 rows=3 pieces, 3 rows=6 pieces."))

    args = parser.parse_args()
    play(args.board_size, args.player_row_span)
