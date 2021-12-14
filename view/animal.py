from random import randint

import pygame.sprite

from view.utils import Colors


class Animal(pygame.sprite.Sprite):
    def __init__(
            self,
            groups,
            animal,
            color
    ):
        self.animal = animal
        self.groups = groups
        self.color = color

        pygame.sprite.Sprite.__init__(self, groups)
        self.rectangle(self.color)

    def rectangle(self, color):
        self.image = pygame.Surface((self.animal.size, self.animal.size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = self.animal.position

    def update(self):
        killed = self.animal.update()

        if killed:
            self.kill()

        self.rect.center = self.animal.position
