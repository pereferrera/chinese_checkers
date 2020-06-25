from copy import deepcopy

from chinese_checkers.pygame_gui import PygameGUI
from chinese_checkers.cc_game import CCGame
from chinese_checkers.cc_reasoner import CCReasoner


class ManualPlayer(CCReasoner):

    def __init__(self, gui: PygameGUI):
        self.gui = gui

    def movement_is_valid(self,
                          from_row: int,
                          from_column: int,
                          to_row: int,
                          to_column: int,
                          game: CCGame,
                          player: int):
        available_moves = self.available_moves(game, player)
        m_game = deepcopy(game)
        m_game._do_move(from_row,
                        from_column,
                        to_row,
                        to_column)
        m_game.rotate_turn()
        for move in available_moves:
            c_game = deepcopy(game)
            c_game.apply_move_sequence(move)
            if c_game == m_game:
                return True
        return False

    def move(self, game: CCGame, player: int):
        valid_move = False
        while not valid_move:
            while not (self.gui.first_click and self.gui.second_click):
                self.gui.update()
            if not self.movement_is_valid(self.gui.first_click[0],
                                          self.gui.first_click[1],
                                          self.gui.second_click[0],
                                          self.gui.second_click[1],
                                          game,
                                          player):
                print('Invalid move, try again')
                self.gui.reset_user_input()
                continue
            # check if movement is valid!
            else:
                game._do_move(self.gui.first_click[0],
                              self.gui.first_click[1],
                              self.gui.second_click[0],
                              self.gui.second_click[1])
                valid_move = True
        self.gui.reset_user_input()
