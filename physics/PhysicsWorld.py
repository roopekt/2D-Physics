from dataclasses import dataclass, field
from .bodies import *
from .collision_detection import get_collisions_between
from .collision_response import update_velocities, update_positions
from pygame.math import Vector2

@dataclass
class PhysicsWorld:
    bodies: list[Rigidbody] = field(default_factory=list)
    gravity: Vector2 = field(default_factory=lambda: Vector2(0.0, -9.807))
    collision_iteration_count: int = 5
    collision_velocity_iteration_count: int = 5
    air_density: float = 1.204

    def advance(self, delta_time):
        for body in self.bodies:
            if not body.is_static:
                #gravity
                body.velocity += self.gravity * delta_time

                #air resistance
                velocity_squared = body.velocity * body.velocity.magnitude()
                body.apply_impulse(-self.air_density * body.drag_coefficient * velocity_squared * delta_time)
                angular_velocity_squared = body.angular_velocity * abs(body.angular_velocity)
                body.apply_angular_impulse(-self.air_density * body.angular_drag_coefficient * angular_velocity_squared * delta_time)

                body.position += body.velocity * delta_time
                body.orientation += body.angular_velocity * delta_time

        for i in range(self.collision_iteration_count):
            self.handle_collisions()

    def handle_collisions(self):
        for i in range(self.collision_iteration_count):
            collisions = self.get_collisions()

            if len(collisions) == 0:
                return

            for i in range(self.collision_velocity_iteration_count):
                any_real_collisions = False
                for collision in collisions:
                    any_real_collisions |= update_velocities(collision)

                if not any_real_collisions:
                    break

            for collision in collisions:
                update_positions(collision)

    def get_collisions(self) -> list[Collision]:
        collisions = []
        for iA, bodyA in enumerate(self.bodies):
            for iB, bodyB in enumerate(self.bodies):
                if iA < iB: #to prevent self collisions and double counting other collisions
                    for colliderA in bodyA.colliders:
                        for colliderB in bodyB.colliders:
                            collisions += get_collisions_between(colliderA, colliderB)

        return collisions
