
from view.bullet import Bullet
from view.abstract import Wander
from view.utils import Colors


class Wolf(Wander):
    def __init__(self, groups, position, size):
        super().__init__(groups, position, size)
        self.max_velocity = 0.4
        self.max_force = 1
        self.color = Colors.DARK_GREY.value
        self.max_hp = 100000

        self.current_hp = self.max_hp

        self.rectangle(self.color)

        self.separation_radius = self.size * 6
        self.alignment_radius = self.size * 0
        self.cohesion_radius = self.size * 0
        self.flee_radius = self.size * 4

    def chose_seek_target(self):
        destinations = {
            animal: (animal.position - self.position).length()
            for animal in self.animals_around
            if not isinstance(animal, Wolf) and not isinstance(animal, Bullet)
        }
        closest_animal = None

        if destinations:
            closest_animal = min(destinations, key=destinations.get)

        return closest_animal

    def check_collision(self, target):
        return (target - self.position).length() < 5

    def fulfill_hp(self):
        self.current_hp = self.max_hp

    def update(self):
        self.forces = []
        self.calculate_animals_around()
        avoid = self.avoid_walls()

        if not self.current_hp:
            self.kill()

        if avoid.length() == 0:
            if self.animals_around:
                target = self.chose_seek_target()
                if target:
                    if self.check_collision(target.position):
                        target.kill()
                        self.fulfill_hp()
                        self.acceleration = self.wandering()
                    else:
                        self.acceleration = self.seek(target.position)
            else:
                self.acceleration = self.wandering()
        else:
            self.acceleration = avoid

        self.current_hp -= 1

        if self.velocity != self.max_velocity:
            self.velocity += self.acceleration
        if self.velocity.length() > self.max_velocity:
            self.velocity.scale_to_length(self.max_velocity)
        self.position += self.velocity
        self.rect.center = self.position

