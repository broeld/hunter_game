from models.abstract import Wander, GroupBehaviours, Flee
from models.rabbit import Rabbit
from models.bullet import Bullet


class Doe(Wander, GroupBehaviours, Flee):
    def __init__(self, groups, position, size):
        super().__init__(groups, position, size)
        self.max_velocity = 0.3
        self.max_force = 1
        self.separation_radius = self.size * 3
        self.alignment_radius = self.size * 5
        self.cohesion_radius = self.size * 10
        self.flee_radius = self.size * 10

    def chose_flee_target(self):
        destinations = {
            animal: (animal.animal.position - self.position).length()
            for animal in self.animals_around
            if not self.check_animal(animal.animal)
        }

        if destinations:
            closest_animal = min(destinations, key=destinations.get)
            return closest_animal
        else:
            return None

    @staticmethod
    def check_animal(animal):
        return isinstance(animal, Rabbit) or isinstance(animal, Doe) or isinstance(animal, Bullet)

    def flock(self):
        animals = [animal for animal in self.animals_around if isinstance(animal.animal, Doe)]
        if animals:
            separation = self.separate(animals) * 0.5
            alignment = self.align(animals) * 0.3
            coh = self.cohesion(animals) * 0.3

            result_force = (separation + alignment + coh) / 3
            self.apply_force(result_force)

    def update(self):
        self.forces = []
        self.calculate_animals_around()

        avoid = self.avoid_walls()

        if avoid.length() == 0:
            if len(self.animals_around) > 0:
                self.flock()
                target = self.chose_flee_target()
                if target is not None:
                    self.acceleration = self.flee(target.animal.position)
            else:
                self.acceleration += self.wandering()
        else:
            self.acceleration = avoid
            
            if len(self.animals_around) > 0:
                target = self.chose_flee_target()
                if target:
                    self.acceleration += self.flee(target.animal.position)

        if self.velocity != self.max_velocity:
            self.velocity += self.acceleration
        if self.velocity.length() > self.max_velocity:
            self.velocity.scale_to_length(self.max_velocity)
        self.position += self.velocity
        self.acceleration *= 0
