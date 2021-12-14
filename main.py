import pygame

from controllers.game_controller import GameController
from view.board import Board
from view.utils import Colors

game_config = dict(
    win_width=1600,
    win_height=900,
    border=100
)

if __name__ == '__main__':
    pygame.init()

    board = Board(
        game_config['win_width'],
        game_config['win_height'],
        game_config['border'],
        Colors.BLACK.value,
        Colors.WHITE.value
    )

    game_controller = GameController(board)
    game_controller.start_game()
