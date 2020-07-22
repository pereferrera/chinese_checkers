from dataclasses import dataclass, field
from typing import List, Tuple
from chinese_checkers.movement import CCMovement


@dataclass
class CCMove:
    board_positions: List[Tuple[int, int]]
    directions: List[CCMovement]


@dataclass(order=True)
class PrioritizedCCMove:
    priority: int
    move: CCMove = field(compare=False)
