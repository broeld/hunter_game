import sys
from random import randint

import pygame

from models.bullet import Bullet
from view.hunter import Hunter
from view.animal import Animal
from models.doe import Doe
from models.hunter import Hunter as HunterModel
from models.rabbit import Rabbit
from view.utils import Colors
from models.wolf import Wolf
from view.board import Board


class GameController:
    def __init__(
            self,
            window
    ):
        self.window = window
        self.all_sprites = pygame.sprite.Group()

    def start_game(self):
        clock = pygame.time.Clock()

        self.window.update_window()
        pygame.display.update()
        pygame.display.flip()

        self.generate_animals(10, 10, 2)

        hunter = Hunter(
            groups=self.all_sprites,
            animal=HunterModel(
                self.all_sprites,
                (self.window.win_width / 2, self.window.win_height / 2),
                20
            ),
            color=Colors.YELLOW.value
        )

        while True:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        Animal(
                            groups=self.all_sprites,
                            animal=Bullet(
                                groups=self.all_sprites,
                                position=hunter.animal.position,
                                size=5,
                                destination_position=mouse_pos
                            ),
                            color=Colors.RED.value
                        )

            if hunter not in self.all_sprites or len(self.all_sprites) == 1:
                text_message = 'You lose:( Press q to quit'

                if hunter in self.all_sprites:
                    text_message = 'You win:) Press q to quit'

                while True:
                    self.window.stop_game(text_message)

                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                pygame.quit()
                                sys.exit()

                    pygame.display.flip()

            self.window.update_window()

            self.all_sprites.update()
            self.check_animals_position()
            self.all_sprites.draw(self.window.window)

            pygame.display.flip()

    def check_animals_position(self):
        for animal in self.all_sprites:
            if (animal.animal.position.x <= self.window.border / 2 or
                    animal.animal.position.x >= self.window.win_width - self.window.border / 2 or
                    animal.animal.position.y <= self.window.border / 2 or
                    animal.animal.position.y >= self.window.win_height - self.window.border / 2):
                animal.kill()

    def generate_animals(self, doe, rabbit, wolf):
        for _ in range(doe):
            Animal(
                groups=self.all_sprites,
                animal=Doe(
                    self.all_sprites,
                    (randint(self.window.border, self.window.win_width - self.window.border),
                     randint(self.window.border, self.window.win_height - self.window.border)),
                    15
                ),
                color=Colors.ORANGE.value
            )

        for _ in range(rabbit):
            Animal(
                groups=self.all_sprites,
                animal=Rabbit(
                    self.all_sprites,
                    (randint(self.window.border, self.window.win_width - self.window.border),
                     randint(self.window.border, self.window.win_height - self.window.border)),
                    15
                ),
                color=Colors.LIGHT_GREY.value
            )

        for _ in range(wolf):
            Animal(
                groups=self.all_sprites,
                animal=Wolf(
                    self.all_sprites,
                    (randint(self.window.border, self.window.win_width - self.window.border),
                     randint(self.window.border, self.window.win_height - self.window.border)),
                    15
                ),
                color=Colors.DARK_GREY.value
            )
