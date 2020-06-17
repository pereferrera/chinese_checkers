import random
import time

from chinese_checkers.cc_game import CCGame
from chinese_checkers.greedy_strategy import GreedyStrategy
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

    game = CCGame(width=6, player_row_spawn=3)

    manual_players = set([2])
    ai_players = {
        1: GreedyStrategy(steps=0, heuristic=combined_heuristic),
        2: GreedyStrategy(steps=0, heuristic=combined_vertical_advance)
    }

    start = time.time()

    player_turn = 2
    game.rotate_turn()

    turns = 0

    gui = PygameGUI(game)
    manual_player = ManualPlayer(gui)

    def print_metrics(player):
        print(f"""
        Player 2:
            cva={combined_vertical_advance(game, player)} 
            iss_cl={inv_squared_sum_center_line(game, player)} 
            iss_dc={inv_squared_sum_dest_corner(game, player)}
        """)

    while(game.state() == 0):
        print(f'Turn: {player_turn}')
        assert game.player_turn == player_turn
        gui.update()
        for player in [1, 2]:
            print_metrics(player)

        if player_turn not in manual_players:
            strategy = ai_players[player_turn]
            move = strategy.select_move(game, player_turn)
            print(f'Move sequence: {move}')
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
