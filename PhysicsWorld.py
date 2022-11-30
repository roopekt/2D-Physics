from dataclasses import dataclass, field
from Rigidbody import Rigidbody
from pygame.math import Vector2

@dataclass
class PhysicsWorld:
    bodies: list[Rigidbody] = field(default_factory=list)
    gravity: Vector2 = field(default_factory=lambda: Vector2(0.0, -9.807))

    def advance(self, deltaTime):
        for body in self.bodies:
            body.velocity += self.gravity * deltaTime
            body.position += body.velocity * deltaTime