from random import randint

import pygame

from models.hunter import Hunter
from models.abstract import Seeker
from view.utils import Colors


class Bullet(Seeker):
    def __init__(
            self,
            groups,
            position,
            size,
            destination_position
    ):
        self.groups = groups
        super().__init__(groups, position, size)

        self.max_velocity = 1
        self.max_force = 0.5
        self.max_distance = 50

        self.velocity = pygame.Vector2(self.max_velocity, 0)
        self.acceleration = self.calculate_acceleration(destination_position)

        self.start_position = position
        self.animals_around = []

    def closest_animal(self):
        destinations = {
            animal: (animal.animal.position - self.position).length()
            for animal in self.animals_around
            if not isinstance(animal.animal, Hunter) and not isinstance(animal.animal, Bullet)
        }

        if destinations:
            return min(destinations, key=destinations.get)
        
        return None

    def calculate_acceleration(self, position):
        return pygame.Vector2(position-self.position).normalize()

    def update(self):
        self.calculate_animals_around()

        if len(self.animals_around) > 0:
            animal = self.closest_animal()
            if animal:
                if (animal.animal.position - self.position).length() < animal.animal.size:
                    animal.kill()
                    return 1

        if (pygame.Vector2(self.position) - pygame.Vector2(self.start_position)).length() > self.max_distance:
            return 1

        if self.velocity != self.max_velocity:
            self.velocity += self.acceleration
        if self.velocity.length() > self.max_velocity:
            self.velocity.scale_to_length(self.max_velocity)

        self.position += self.velocity
