import abc
from chinese_checkers.cc_game import CCGame


class CCHeuristic(metaclass=abc.ABCMeta):

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
