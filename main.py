from controllers.game_controller import GameController

# Make game_config in such way because it is impossible to create .exe file with .yaml config
game_config = dict(
    win_width=1600,
    win_height=900,
    border=100
)

if __name__ == '__main__':
    game_controller = GameController(game_config)
    game_controller.start_game()
