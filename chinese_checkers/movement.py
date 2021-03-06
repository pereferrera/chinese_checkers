from enum import Enum

"""
Represents a single possible movement of a piece in the board
"""


class CCMovement(Enum):
    L = 1  # left
    R = 2  # right
    LN = 3  # left-north
    RN = 4  # right-north
    LS = 5  # left-south
    RS = 6  # right-south
