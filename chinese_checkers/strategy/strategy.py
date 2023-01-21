import abc
from chinese_checkers.game import CCGame
from chinese_checkers.reasoner import CCReasoner
from chinese_checkers.move import CCMove


class CCStrategy(CCReasoner, metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'select_move') and
                callable(subclass.on_move) or
                NotImplementedError)

    @abc.abstractmethod
    def select_move(self, game: CCGame, player: int) -> CCMove:
        raise NotImplementedError
