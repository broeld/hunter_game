import pygame

from view.abstract import Seeker
from view.utils import Colors


class Hunter(Seeker):
    def __init__(
            self,
            groups,
            position,
            size
    ):
        super().__init__(groups, position, size)

        self.max_velocity = 1
        self.max_force = 1
        self.color = Colors.YELLOW.value
        self.destination = self.position

        self.rectangle(self.color)

    def update(self):
        desire = pygame.mouse.get_pos()
        self.acceleration = self.seek([desire[0]-1, desire[1]-1])

        if self.velocity != self.max_velocity:
            self.velocity += self.acceleration
        if self.velocity.length() > self.max_velocity:
            self.velocity.scale_to_length(self.max_velocity)
        self.position += self.velocity
        if self.position.x > 1600:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = 1600
        if self.position.y > 900:
            self.position.y = 0
        if self.position.y < 0:
            self.position.y = 900
        self.rect.center = self.position

