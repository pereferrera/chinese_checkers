from chinese_checkers.cc_game import CCGame

"""
TODO Make an interface for heuristics so it's clearer what we need to 
provide to strategies

Reminder: heuristics here are to be maximized, not minimized
"""


def combined_heuristic(game: CCGame, player: int, weights: list=[0.1,
                                                                 0.899,
                                                                 0.001]):
    # rough normalization to combine different heuristics
    return (
        weights[0] * inv_squared_sum_dest_corner(game, player) +
        weights[1] * combined_vertical_advance(game, player) +
        weights[2] * inv_squared_sum_center_line(game, player)
    )


def combined_vertical_advance(game: CCGame, player: int):
    """
    Returns:
    -------
    float
        The sum of vertical advance for all pieces of the passed player,
        as metric between 1 and 0
    """
    heigth = len(game.board)
    combined_va = 0
    pieces = 0
    for row in range(0, heigth):
        for column in range(0, len(game.board[row])):
            if game.board[row][column] == player:
                pieces += 1
                combined_va += (
                    row if player == 1 else (heigth - row - 1)
                )
    return combined_va / (heigth * pieces)


def inv_squared_sum_center_line(game: CCGame, player: int):
    """
    Returns:
    -------
    float
        The inverse squared sum of the distances of all pieces from this player
        to the center line.
    """
    squared_sum = 0

    heigth = len(game.board)

    for row in range(0, heigth):
        center = (len(game.board[row]) / 2)
        for column in range(0, len(game.board[row])):
            if game.board[row][column] == player:
                dist = abs(column - center)
                squared_sum += (dist * dist)

    if squared_sum == 0:
        return 1
    return min(1, 1 / squared_sum)


def inv_squared_sum_dest_corner(game: CCGame, player: int):
    """
    Returns:
    -------
    float
        The inverse squared sum of the distances of all pieces from this player
        to its destiny corner (0,0) or (n,0).
    """
    squared_sum = 0

    heigth = len(game.board)
    dest_row = heigth - 1
    dest_column = 0

    if player == 2:
        dest_row = 0

    for row in range(0, heigth):
        for column in range(0, len(game.board[row])):
            if game.board[row][column] == player:
                dist = max(abs(dest_row - row),
                           abs(dest_column - column))
                squared_sum += (dist * dist)

    return min(1, 1 / squared_sum)
