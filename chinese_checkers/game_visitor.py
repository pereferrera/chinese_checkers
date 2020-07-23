import abc


class GameVisitor(metaclass=abc.ABCMeta):
    """
    Implements a visitor pattern for classes that need to be aware of
    the movements that happen during the game (e.g. stateful heuristics).
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'on_move') and
                callable(subclass.on_move) and
                hasattr(subclass, 'on_init_game') and
                callable(subclass.on_init_game) or
                NotImplemented)

    @abc.abstractmethod
    def on_init_game(self,
                     board: list):
        raise NotImplemented

    @abc.abstractmethod
    def on_move(self,
                from_row: int,
                from_column: int,
                dest_row: int,
                dest_column: int,
                player: int):
        raise NotImplementedError
