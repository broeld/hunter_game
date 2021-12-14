from random import randint

import pygame

from view.hunter import Hunter
from view.abstract import Seeker
from view.utils import Colors


class Bullet(Seeker):
    def __init__(
            self,
            groups,
            position,
            size,
            mouse_position
    ):
        self.groups = groups
        super().__init__(groups, position, size)

        self.max_velocity = 1
        self.max_force = 1
        self.color = Colors.RED

        self.rectangle(self.color)

        self.velocity = pygame.Vector2(self.max_velocity, 0)
        self.acceleration = pygame.Vector2(0, 0)

        self.cohesion_radius = self.size * 3
        self.separation_radius = self.size * 1
        self.alignment_radius = self.size * 2
        self.flee_radius = self.size * 10

        self.target = pygame.Vector2(mouse_position)
        self.animals_around = []
        self.forces = []

    def chose_seek_target(self):
        destinations = {
            animal: (animal.position - self.position).length()
            for animal in self.animals_around
            if not isinstance(animal, Hunter) and not isinstance(animal, Bullet)
        }
        closest_animal = None

        if destinations:
            closest_animal = min(destinations, key=destinations.get)

        return closest_animal

    def update(self):
        self.acceleration = self.seek(self.target)

        self.calculate_animals_around()

        if len(self.animals_around) > 0:
            animal = self.chose_seek_target()
            if animal:
                if (animal.position - self.position).length() < animal.size:
                    animal.kill()
                    self.kill()

        if (pygame.Vector2(self.position) - pygame.Vector2(self.target)).length() < 1:
            self.kill()

        if self.velocity != self.max_velocity:
            self.velocity += self.acceleration
        if self.velocity.length() > self.max_velocity:
            self.velocity.scale_to_length(self.max_velocity)
        self.position += self.velocity
        if self.position.x > 1550 or self.position.x < 50 or self.position.y > 850 or self.position.y < 50:
            self.kill()
            return
        self.rect.center = self.position

