import random
import time

from scipy import stats

from chinese_checkers.cc_game import CCGame
from chinese_checkers.min_max_strategy import MinMaxStrategy
from chinese_checkers.pygame_gui import PygameGUI
from chinese_checkers.manual_player import ManualPlayer
from chinese_checkers.oc_heuristic import OptimizedCombinedHeuristic


if __name__ == "__main__":
    random.seed(1)

    heuristic = OptimizedCombinedHeuristic()
    game = CCGame(width=9, player_row_spawn=4, visitors=[heuristic])

#    manual_players = set([2])
    manual_players = set()


    ai_players = {
        1: MinMaxStrategy(steps=1, pre_sort_moves=True, heuristic=heuristic),
        2: MinMaxStrategy(steps=1, pre_sort_moves=True, heuristic=heuristic)
    }

    start = time.time()

    player_turn = 1

    turns = 0

    gui = PygameGUI(game)
    manual_player = ManualPlayer(gui)

    ai_players_perf = {
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
