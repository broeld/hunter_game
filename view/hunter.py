import pygame

from view.animal import Animal
from view.utils import Colors


class Hunter(Animal):
    def __init__(
            self,
            groups,
            animal,
            color
    ):
        super().__init__(groups, animal, color)

    def update(self):
        desired = pygame.mouse.get_pos()
        self.animal.update(desired)
        self.rect.center = self.animal.position
