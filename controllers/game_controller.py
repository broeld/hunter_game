import sys
from random import randint

import pygame

from view.bullet import Bullet
from view.hunter import Hunter
from view.doe import Doe
from view.rabbit import Rabbit
from view.wolf import Wolf


class GameController:
    def __init__(
            self,
            game_config
    ):
        self.game_config = game_config
        self.win_width = self.game_config['win_width']
        self.win_height = self.game_config['win_height']
        self.border = self.game_config['border']
        self.all_sprites = pygame.sprite.Group()
        self.window = None
        self.surface = None

    def start_game(self, all_sprites=None):
        self.init_game()
        clock = pygame.time.Clock()
        self.init_windows(
            self.win_width,
            self.win_height,
            self.border,
            Colors.BLACK,
            Colors.WHITE
        )

        pygame.display.flip()

        self.generate_animals(10, 10, 2)

        hunter = Hunter(self.all_sprites, (self.win_width/2, self.win_height/2), 20)

        while True:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        Bullet(self.all_sprites, hunter.position, 5, mouse_pos)

            self.update_window(
                Colors.BLACK,
                Colors.WHITE,
                self.border
            )

            self.all_sprites.update()
            self.all_sprites.draw(self.window)

            pygame.display.flip()

    @staticmethod
    def init_game():
        pygame.init()
        pygame.font.init()

    def init_windows(self, win_width, win_height, border, bg_color, surf_color):
        pygame.display.set_caption("Hunter")

        self.window = pygame.display.set_mode((win_width, win_height))
        self.surface = pygame.Surface((win_width - border, win_height - border))

        self.update_window(bg_color, surf_color, border)
        pygame.display.update()

    def update_window(self, bg_color, surf_color, border):
        self.window.fill(bg_color)
        self.surface.fill(surf_color)
        self.window.blit(self.surface, (border/2, border/2))

    def generate_animals(self, doe, rabbit, wolf):
        for _ in range(doe):
            Doe(
                self.all_sprites,
                (randint(self.border, self.win_width - self.border),
                 randint(self.border, self.win_height - self.border)),
                15
            )

        for _ in range(rabbit):
            Rabbit(
                self.all_sprites,
                (randint(self.border, self.win_width - self.border),
                 randint(self.border, self.win_height - self.border)),
                15
            )

        for _ in range(wolf):
            Wolf(
                self.all_sprites,
                (randint(self.border, self.win_width - self.border),
                 randint(self.border, self.win_height - self.border)),
                15
            )
