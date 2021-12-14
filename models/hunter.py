import pygame

from models.abstract import Seeker
from view.utils import Colors


class Hunter(Seeker):
    def __init__(
            self,
            groups,
            animal,
            color
    ):
        super().__init__(groups, animal, color)

        self.max_velocity = 0.5
        self.max_force = 1
        self.destination = self.position

    def update(self, desired):
        self.acceleration = self.seek([desired[0]-1, desired[1]-1])

        if self.velocity != self.max_velocity:
            self.velocity += self.acceleration
        if self.velocity.length() > self.max_velocity:
            self.velocity.scale_to_length(self.max_velocity)
        self.position += self.velocity
