import abc

from chinese_checkers.game import CCGame


class CCHeuristic(metaclass=abc.ABCMeta):
    """
    Provide a value between 0 and 1, to be maximized (1 is best-looking board)
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'value') and
                callable(subclass.value) or
                NotImplemented)

    @abc.abstractmethod
    def value(self,
              game: CCGame,
              player: int):
        raise NotImplementedError
