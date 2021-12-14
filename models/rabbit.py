from models.abstract import Wander, Flee
from models.bullet import Bullet


class Rabbit(Wander, Flee):
    def __init__(self, groups, position, size):
        super().__init__(groups, position, size)
        self.max_velocity = 0.3
        self.max_force = 1

        self.separation_radius = self.size * 3
        self.alignment_radius = self.size * 0
        self.cohesion_radius = self.size * 0
        self.flee_radius = self.size * 2

    def chose_flee_target(self):
        destinations = {
            animal: (animal.animal.position - self.position).length()
            for animal in self.animals_around
            if not isinstance(animal.animal, Bullet)
        }

        if destinations:
            return min(destinations, key=destinations.get).animal.position

        return None

    def update(self):
        self.forces = []
        self.calculate_animals_around()
        avoid = self.avoid_walls()

        if avoid.length() == 0:
            if len(self.animals_around) > 0:
                target = self.chose_flee_target()
                if target:
                    self.acceleration = self.flee(target)
            else:
                self.acceleration += self.wandering()
        else:
            self.acceleration = avoid

            if len(self.animals_around) > 0:
                target = self.chose_flee_target()
                if target:
                    self.acceleration += self.flee(target)

        if self.velocity != self.max_velocity:
            self.velocity += self.acceleration
        if self.velocity.length() > self.max_velocity:
            self.velocity.scale_to_length(self.max_velocity)
        self.position += self.velocity
        self.acceleration *= 0
