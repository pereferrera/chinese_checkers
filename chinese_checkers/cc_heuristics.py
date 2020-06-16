from chinese_checkers.cc_game import CCGame


def combined_vertical_advance(game: CCGame, player: int):
    """
    Returns:
    -------
    int
        The sum of vertical advance for all pieces of the passed player
    """
    heigth = len(game.board)
    combined_va = 0
    for row in range(0, heigth):
        for column in range(0, len(game.board[row])):
            if game.board[row][column] == player:
                combined_va += (
                    row if player == 1 else (heigth - row - 1)
                )
    return combined_va
