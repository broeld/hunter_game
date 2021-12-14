from random import uniform

import pygame

from models.animal import Animal
from view.utils import WanderingConst


class Seeker(Animal):
    def seek(self, target):
        return self.calculate_steer(target)


class Flee(Animal):
    def flee(self, target):
        return self.calculate_steer(target) * (-1)


class Wander(Seeker):
    def wandering(self):
        future = self.position + self.velocity.normalize() * WanderingConst.WANDERING_DISTANCE.value
        target = future + pygame.Vector2(WanderingConst.WANDERING_RADIUS.value, 0).rotate(uniform(0, 360))
        self.target = target
        return self.seek(target)


class GroupBehaviours(Seeker):
    def separate(self, animals):
        desired = pygame.Vector2(0, 0)
        animals_count = 0
        for animal in animals:
            animal_destination = animal.animal.position - self.position
            if animal_destination.length() != 0 and animal_destination.length() < self.separation_radius:
                animal_destination.normalize()
                desired -= animal_destination
                animals_count += 1

        if animals_count > 1:
            desired /= animals_count
            desired -= self.velocity

        if desired.length() >= self.max_force:
            desired.scale_to_length(self.max_force)

        return desired

    def cohesion(self, animals):
        desired = pygame.Vector2(0, 0)
        animals_count = 0
        for animal in animals:
            animal_destination = animal.animal.position - self.position
            if animal_destination.length() != 0 and animal_destination.length() < self.cohesion_radius:
                desired += animal_destination
                animals_count += 1

        if animals_count > 0:
            desired /= animals_count
            desired -= self.velocity

        if desired.length() > self.max_force:
            desired.scale_to_length(self.max_force)

        return desired

    def align(self, animals):
        align_count = 0
        desired = pygame.Vector2(0, 0)
        for animal in animals:
            distance = (animal.animal.position - self.position).length()
            if distance < self.alignment_radius:
                align_count += 1
                desired += animal.animal.velocity

        if align_count > 0:
            desired /= align_count
            desired.scale_to_length(self.max_velocity)
            desired -= self.velocity

        if desired.length() > self.max_force:
            desired.scale_to_length(self.max_force)

        return desired
