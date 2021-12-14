import pygame
from random import randint


class Animal:
    def __init__(
            self,
            groups,
            position,
            size
    ):
        self.groups = groups
        self.position = pygame.Vector2(position)

        self.size = size
        self.max_velocity = 1
        self.max_force = 1

        self.velocity = pygame.Vector2(self.max_velocity, 0)
        self.acceleration = pygame.Vector2(0, 0)

        self.cohesion_radius = self.size * 3
        self.separation_radius = self.size * 1
        self.alignment_radius = self.size * 2
        self.flee_radius = self.size * 10

        self.target = pygame.Vector2(randint(0, 1600), randint(0, 800))
        self.animals_around = []
        self.forces = []

    def calculate_animals_around(self):
        self.animals_around = []
        animals = self.groups.sprites()
        for animal in animals:
            distance = (animal.animal.position - self.position).length()
            if distance < max(self.cohesion_radius, self.alignment_radius, self.separation_radius, self.flee_radius) \
                    and distance != 0:
                self.animals_around.append(animal)
                animal.animal.animals_around.append(self)

    def calculate_steer(self, target):
        desired = (target - self.position).normalize()
        steer = (desired - self.velocity)
        if steer.length() > self.max_force:
            steer.scale_to_length(self.max_force)

        return steer

    def apply_force(self, force):
        self.forces.append(force)
        self.acceleration += force

    def avoid_walls(self, max_x=1600, max_y=900):
        steer = pygame.Vector2(0, 0)
        desired = pygame.Vector2(0, 0)
        near_wall = False

        limit = 100

        if self.position.x < limit:
            desired = pygame.Vector2(-self.velocity.x, self.velocity.y)
            near_wall = True
        if self.position.x > max_x - limit:
            desired = pygame.Vector2(-self.velocity.x, self.velocity.y)
            near_wall = True
        if self.position.y < limit:
            desired = pygame.Vector2(self.velocity.x, -self.velocity.y)
            near_wall = True
        if self.position.y > max_y - limit:
            desired = pygame.Vector2(self.velocity.x, -self.velocity.y)
            near_wall = True

        if near_wall:
            steer = desired - self.velocity
            if steer.length() > self.max_force:
                steer.scale_to_length(self.max_force)

        return steer

    def arrive(self, target):
        steer = self.calculate_steer(target)
        if steer.normalize() > self.max_force:
            return (steer / steer.normalize()).scale_to_length(self.max_force)

        return steer
