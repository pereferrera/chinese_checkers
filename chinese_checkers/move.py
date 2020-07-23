from dataclasses import dataclass, field
from typing import List, Tuple
from chinese_checkers.movement import CCMovement


@dataclass
class CCMove:
    """
    Represents a full move from a player, which might span different
    positions on the board (in the case of jumping).

    note: len(board_positions) == len(directions) - 1
    , though not explicitly enforced anywhere

    First position of the move is the origin where the piece is, before
    being moved.
    """
    board_positions: List[Tuple[int, int]]
    directions: List[CCMovement]


@dataclass(order=True)
class PrioritizedCCMove:
    priority: int
    move: CCMove = field(compare=False)
