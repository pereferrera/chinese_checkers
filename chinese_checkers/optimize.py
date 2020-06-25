from copy import deepcopy
from functools import partial
import itertools
import random
from collections import Counter

from chinese_checkers.cc_game import CCGame

import numpy as np
from chinese_checkers.cc_heuristics import combined_heuristic
from chinese_checkers.min_max_strategy import MinMaxStrategy

"""
Explorations on finding optimal weights for the combined heuristic
in cc_heuristics using a genetic algorithm-oriented approach.

TODO: Validate some of the code here through unit tests.
"""
if __name__ == "__main__":
    random.seed(1)
    N_WEIGHTS = 3
    LOOK_AHEAD = 1
    GENERATION_SIZE = 12
    RANDOM_FILL_SIZE = 4
    SELECT_BEST = 4
    COMPETE_AGAINST = 3
    GAME_WIDTH = 9
    PLAYER_ROW_SPAWN = 3

    def random_individual():
        """
        Returns a list of weights between 0 and 1, all weights sum 1
        """
        return list(np.random.dirichlet(np.ones(N_WEIGHTS), size=1)[0])

    def compete(weights_1: list, weights_2: list):
        """
        Plays a game between two AIs with different weights and return
        the result of the game
        """
        print('{} versus {}'.format(weights_1, weights_2))
        game = CCGame(width=GAME_WIDTH, player_row_spawn=PLAYER_ROW_SPAWN)
        heuristic_1 = partial(combined_heuristic,
                              weights=weights_1)
        heuristic_2 = partial(combined_heuristic,
                              weights=weights_2)

        strategy_1 = MinMaxStrategy(
            steps=LOOK_AHEAD, pre_sort_moves=True,
            heuristic=heuristic_1)
        strategy_2 = MinMaxStrategy(
            steps=LOOK_AHEAD, pre_sort_moves=True,
            heuristic=heuristic_2)

        turns = 0

        last_boards = set()
        board_repeats = 0

        while(game.state() == 0):
            strategy = strategy_1 if game.player_turn == 1 else strategy_2
            move = strategy.select_move(game, game.player_turn)
            game.apply_move_sequence(move)
            if game in last_boards:
                board_repeats += 1

            if board_repeats == 3:
                # infinite loop (tie)
                print('Board repeats - tie')
                return -1

            last_boards.add(deepcopy(game))
            turns += 1

        print(f'{game.state()} wins')
        return game.state()

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

        while True:
            print(f'Generation {n_generations}')
            generation = [random_individual()
                          for i in range(0, GENERATION_SIZE)]
            scores = Counter()
            played_against = {}

            for i in range(0, GENERATION_SIZE):
                # (this doesn't guarantee that everybody will play exactly
                #  COMPETE_AGAINST matches. There might be more)
                while len(played_against.get(i, [])) < COMPETE_AGAINST:
                    adversaries = (list(
                        set(list(range(0, i)) +
                            list(range(i + 1, GENERATION_SIZE))) -
                        set(played_against.get(i, []))
                    ))
                    against = random.choice(adversaries)

                    result = compete(generation[i], generation[against])
                    played_against[i] = played_against.get(i, []) + [against]
                    played_against[against] = (
                        played_against.get(against, []) + [i]
                    )

                    if result == 1:
                        scores[i] += 10
                    elif result == 2:
                        scores[against] += 10
                    else:
                        # tie
                        scores[i] += 1
                        scores[against] += 1

            # select at most X population for the next generation
            best = [a[0]
                    for a in scores.most_common(n=SELECT_BEST)]

            print(f'{len(best)} candidates selected for next generation.')
            next_generation = [generation[b] for b in best]

            # fill with offspring from the best candidates
            for pair in itertools.permutations(best, 2):
                next_generation.append(
                    crossover_avg(generation[pair[0]],
                                  generation[pair[1]]))
                print(f'Offspring generated: {pair}')
                if len(next_generation) == GENERATION_SIZE - RANDOM_FILL_SIZE:
                    break

            for i in range(len(next_generation), GENERATION_SIZE):
                # fill the remaining space for the next generation with
                # random individuals
                print('Random individual generated')
                next_generation.append(random_individual())

            assert len(generation) == GENERATION_SIZE
            generation = next_generation
            n_generations += 1

    genetic_search()
