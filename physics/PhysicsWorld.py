from dataclasses import dataclass, field
from .Rigidbody import Rigidbody
from .collision import Collision
from pygame.math import Vector2

@dataclass
class PhysicsWorld:
    bodies: list[Rigidbody] = field(default_factory=list)
    gravity: Vector2 = field(default_factory=lambda: Vector2(0.0, -9.807))
    collision_iteration_count: int = 5

    def advance(self, delta_time):
        for body in self.bodies:
            if not body.is_static:
                body.velocity += self.gravity * delta_time
                body.position += body.velocity * delta_time
                body.orientation += body.angular_velocity * delta_time

        for i in range(self.collision_iteration_count):
            self.handle_collisions()

    def handle_collisions(self):
        collisions = self.get_collisions()

        for collision in collisions:
            collision.update_velocities()

        for collision in collisions:
            collision.update_positions()

    def get_collisions(self) -> list[Collision]:
        collisions = []
        for iA, bodyA in enumerate(self.bodies):
            for iB, bodyB in enumerate(self.bodies):
                if iA < iB: #to prevent self collisions and double counting other collisions
                    for colliderA in bodyA.colliders:
                        for colliderB in bodyB.colliders:
                            collisions += colliderA.get_collisions_with(colliderB)

        return collisions
