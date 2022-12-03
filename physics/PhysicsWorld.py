from dataclasses import dataclass, field
from .Rigidbody import Rigidbody
from pygame.math import Vector2

@dataclass
class PhysicsWorld:
    bodies: list[Rigidbody] = field(default_factory=list)
    gravity: Vector2 = field(default_factory=lambda: Vector2(0.0, -9.807))

    def advance(self, delta_time):
        for body in self.bodies:
            if not body.is_static:
                body.velocity += self.gravity * delta_time
                body.position += body.velocity * delta_time