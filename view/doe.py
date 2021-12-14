from random import uniform

import pygame

from view.abstract import Wander, Flee, GroupBehaviors
from view.rabbit import Rabbit


class Doe(Wander, GroupBehaviors, Flee):
    def __init__(self, groups, position, size):
        super().__init__(groups, position, size)
        self.max_velocity = 0.3
        self.max_force = 1
        self.color = Colors.ORANGE

        self.rectangle(self.color)

        self.separation_radius = self.size * 5
        self.alignment_radius = self.size * 5
        self.cohesion_radius = self.size * 15
        self.flee_radius = self.size * 10

    def chose_flee_target(self):
        destinations = {
            animal: (animal.position - self.position).length()
            for animal in self.animals_around
            if not self.check_animal(animal)
        }

        if destinations:
            closest_animal = min(destinations, key=destinations.get)
            return closest_animal
        else:
            return None

    @staticmethod
    def check_animal(animal):
        return isinstance(animal, Rabbit) or isinstance(animal, Doe)

    def flock(self):
        animals = [animal for animal in self.animals_around if isinstance(animal, Doe)]
        separation = self.separate(animals) * 0.4
        alignment = self.align(animals) * 0.3
        coh = self.cohesion(animals) * 0.9

        self.apply_force(separation)
        self.apply_force(alignment)
        self.apply_force(coh)

    def update(self):
        self.forces = []
        self.calculate_animals_around()
        avoid = self.avoid_walls()

        if avoid.length() == 0:
            if len(self.animals_around) > 0:
                target = self.chose_flee_target()
                if target is not None:
                    self.acceleration = self.flee(target.position)
            else:
                self.acceleration += self.wandering()
        else:
            if len(self.animals_around) > 0:
                target = self.chose_flee_target()
                if target:
                    self.acceleration = self.flee(target.position)

            self.acceleration += avoid

        self.flock()

        if self.velocity != self.max_velocity:
            self.velocity += self.acceleration
        if self.velocity.length() > self.max_velocity:
            self.velocity.scale_to_length(self.max_velocity)
        self.position += self.velocity
        self.rect.center = self.position

    def rectangle(self, color):
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
