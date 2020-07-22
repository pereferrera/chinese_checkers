import itertools
import random
from typing import Set
from copy import deepcopy
from collections import Counter

import numpy as np

from chinese_checkers.game import CCGame
from chinese_checkers.min_max_strategy import MinMaxStrategy
from chinese_checkers.oc_heuristic import OptimizedCombinedHeuristic
from chinese_checkers.only_max_strategy import OnlyMaxStrategy

"""
Script for finding optimal weights for the combined heuristic
 using a genetic-inspired search. Random weights are generated which then
 compete against a greedy strategy based on vertical advance.
 The ones that win the game in as few movements as possible stay for the
 next generation. New crossed-over weights are generated as well
 (offspring).
"""
if __name__ == "__main__":
    random.seed(1)
    N_WEIGHTS = 3
    LOOK_AHEAD = 1
    GENERATION_SIZE = 12
    RANDOM_FILL_SIZE = 4
    SELECT_BEST = 4
    GAME_WIDTH = 7
    # deliberately small number of pieces to avoid high probability of tie
    PLAYER_ROW_SPAN = 3
    MAX_TURNS = 200

    def random_individual():
        """
        Returns a list of weights between 0 and 1, all weights sum 1
        """
        return list(np.random.dirichlet(np.ones(N_WEIGHTS), size=1)[0])

    def compete(weights_1: list, weights_2: list):
        """
        Plays a game between two AIs with different weights and return
        the result of the game.
        The second AI is in disadvantage (has a pure greedy lookahead).

        Return the number of turns it took for player 1 to beat player 2,
        or MAX_TURNS if player 1 didn't manage to beat player 2.
        """
        print('{} versus greedy {}'.format(weights_1, weights_2))

        heuristic_1 = OptimizedCombinedHeuristic(weights_1)
        heuristic_2 = OptimizedCombinedHeuristic(weights_2)

        game = CCGame(width=GAME_WIDTH,
                      player_row_span=PLAYER_ROW_SPAN,
                      visitors=[heuristic_1, heuristic_2])

        strategy_1 = MinMaxStrategy(
            steps=LOOK_AHEAD, pre_sort_moves=True,
            transposition_table=True,
            heuristic=heuristic_1)
        strategy_2 = OnlyMaxStrategy(
            player=2,
            steps=0,
            transposition_table=True,
            heuristic=heuristic_2)

        turns = 0

        last_boards: Set[CCGame] = set()
        board_repeats = 0

        while(game.state() == 0 and turns < MAX_TURNS):
            strategy = (
                strategy_1 if game.player_turn == 1 else strategy_2
            )
            move = strategy.select_move(game, game.player_turn)
            game.apply_move_sequence(move)
            if game in last_boards:
                board_repeats += 1

            if board_repeats == 3:
                # infinite loop (tie)
                print('Board repeats - tie')
                return MAX_TURNS

            last_boards.add(deepcopy(game))
            turns += 1

        state = game.state()
        if state == 1:
            print(f'Won in {turns} turns.')
            return min(MAX_TURNS, turns)
        else:
            print(f'Failed to beat player 2, game state: {state}')
            return MAX_TURNS

    def crossover_avg(weights_1: list, weights_2: list):
        """
        Return crossed-over weights from the two input weights lists
        """
        return [np.average([weights_1[i],
                            weights_2[i]]) for i in range(0, len(weights_1))]

    def genetic_search():
        """
        Genetic search of optimal weights, right now implemented as an
        infinite loop (results to be gathered via stdout).
        """
        n_generations = 0

        generation = [random_individual()
                      for i in range(0, GENERATION_SIZE)]

        while True:
            print(f'Generation {n_generations}: {generation}')

            scores = Counter()

            for i in range(0, GENERATION_SIZE):
                n_turns = compete(generation[i], [0.0, 1.0, 0.0])
                scores[i] += MAX_TURNS - n_turns

            # select at most X population for the next generation
            best = [a[0]
                    for a in scores.most_common(n=SELECT_BEST)]

            print(f'{len(best)} candidates selected for next generation.')
            next_generation = [generation[b] for b in best]

            # fill with offspring from the best candidates
            for pair in itertools.combinations(best, 2):
                next_generation.append(
                    crossover_avg(generation[pair[0]],
                                  generation[pair[1]]))
                print(f'Offspring generated between: {pair}')
                if len(next_generation) == GENERATION_SIZE - RANDOM_FILL_SIZE:
                    break

            for i in range(len(next_generation), GENERATION_SIZE):
                # fill the remaining space for the next generation with
                # random individuals
                next_generation.append(random_individual())

            assert len(generation) == GENERATION_SIZE
            generation = next_generation
            n_generations += 1

    genetic_search()
