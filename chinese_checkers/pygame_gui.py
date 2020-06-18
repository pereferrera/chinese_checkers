import pygame

from chinese_checkers.cc_game import CCGame


class PygameGUI():

    BLOCK_SIZE = 50  # Sets the size of the grid block

    BLACK = (0, 0, 0)

    EMPTY = (100, 100, 100)
    PLAYER_1 = (10, 200, 10)
    PLAYER_2 = (200, 10, 10)

    def __init__(self, game: CCGame):
        self.game = game
        pygame.init()
        self.window_width = len(self.game.board) * self.BLOCK_SIZE
        self.window_height = self.game.width * self.BLOCK_SIZE

        self.screen = pygame.display.set_mode((self.window_height,
                                               self.window_width))
        self.screen.fill(self.BLACK)
        self.exit_gui = False
        self.reset_user_input()

    def reset_user_input(self):
        self.first_click = None
        self.second_click = None

    def handle_left_click(self, x: int, y: int):
        row = int(y / self.BLOCK_SIZE)
        column = int((x - (self.game.width -
                           len(self.game.board[row])) *
                      (self.BLOCK_SIZE / 2)) / self.BLOCK_SIZE)
        print('{} {}'.format(row, column))
        if not self.first_click:
            self.first_click = (row, column)
        elif not self.second_click and (row, column) != self.first_click:
            self.second_click = (row, column)

    def update(self):
        if self.exit_gui:
            raise Exception('User exited GUI')

        def draw_board(board, board_width):
            for row in range(len(board)):
                for column in range(len(board[row])):
                    spacing = board_width - len(board[row])
                    if board[row][column] == 1:
                        color = self.PLAYER_1
                    elif board[row][column] == 2:
                        color = self.PLAYER_2
                    else:
                        color = self.EMPTY
                    x = int((self.BLOCK_SIZE / 2) +
                            column * self.BLOCK_SIZE +
                            spacing * (self.BLOCK_SIZE / 2))
                    y = int((self.BLOCK_SIZE / 2) + row *
                            self.BLOCK_SIZE)
                    pygame.draw.circle(self.screen,
                                       color,
                                       (x, y),
                                       int(self.BLOCK_SIZE / 2))

        draw_board(self.game.board, self.game.width)
        pygame.time.wait(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.exit_gui = True
                break

        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            self.handle_left_click(x, y)

        # update board if needed
        pygame.display.update()
