import pygame

from view.bullet import Bullet
from view.abstract import Wander, Flee
from view.utils import Colors


class Rabbit(Wander, Flee):
    def __init__(self, groups, position, size):
        super().__init__(groups, position, size)
        self.max_velocity = 0.6
        self.max_force = 1
        self.color = Colors.LIGHT_GREY.value

        self.rectangle(self.color)

        self.separation_radius = self.size * 3
        self.alignment_radius = self.size * 0
        self.cohesion_radius = self.size * 0
        self.flee_radius = self.size * 2

    def chose_flee_target(self):
        destinations = {
            animal: (animal.position - self.position).length()
            for animal in self.animals_around
            if not isinstance(animal, Bullet)
        }

        if destinations:
            return min(destinations, key=destinations.get).position

        return None

    def update(self):
        self.forces = []
        self.calculate_animals_around()
        avoid = self.avoid_walls()

        if avoid.length() == 0:
            if len(self.animals_around) > 0:
                target = self.chose_flee_target()
                if target:
                    self.acceleration = self.flee(target) * 4
            else:
                self.acceleration += self.wandering()
        else:
            self.acceleration = avoid

            if len(self.animals_around) > 0:
                target = self.chose_flee_target()
                if target:
                    self.acceleration += self.flee(target)
                    self.acceleration /= 2

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

    def rectangle(self, color):
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = self.position



