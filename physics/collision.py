from dataclasses import dataclass, field
from pygame.math import Vector2
from utility import zero_vector_factory, divide_vectors_as_complex, multiply_vectors_as_complex

@dataclass
class Collider:
    offset: Vector2 = field(default_factory=zero_vector_factory)
    angle_offset: float = 0
    elasticity: float = 0.3
    rest_friction_coefficient: float = 0.3
    dynamic_friction_coefficient: float = 0.2
    rigidbody: object = field(init=False)

    def position(self):
        return self.rigidbody.position + self.offset.rotate_rad(self.rigidbody.orientation)

    def orientation(self):
        return self.rigidbody.orientation + self.angle_offset

    def get_collisions_with(self, other):
        if self.rigidbody.is_static and other.rigidbody.is_static:
            return []

        if isinstance(self, CircleCollider) and isinstance(other, CircleCollider):
            return get_collisions_circle_circle(self, other)
        else:
            raise Exception(f"Can't check collision between a {type(self)} and a {type(other)}.")

@dataclass
class Collision:
    bodyA: Collider
    bodyB: Collider
    collision_point: Vector2 #world space
    penetration_distance: float
    normal: Vector2 #surface normal of bodyA (outwards pointing) at collision_point

    def update_velocities(self):
        relative_velocity: Vector2 = (self.bodyB.rigidbody.velocity_at_point(self.collision_point)
                                    - self.bodyA.rigidbody.velocity_at_point(self.collision_point))
        relative_velocity = divide_vectors_as_complex(relative_velocity, self.normal) #rotate so that x is in the direction of the normal
        reaction_impulse = Vector2(0.0)

        if relative_velocity.x > 0.0:
            print("WARNING: collision between objects moving away from each other")
            return

        #bounce
        velocity_change_for_unit_impulse = (self.bodyA.rigidbody.apply_test_impulse( self.normal, self.collision_point)
                                          + self.bodyB.rigidbody.apply_test_impulse(-self.normal, self.collision_point))
        elasticity = max(self.bodyA.elasticity, self.bodyB.elasticity)
        target_velocity_change = (1 + elasticity) * relative_velocity.x
        reaction_impulse.x = target_velocity_change / velocity_change_for_unit_impulse

        #TODO: friction

        #apply the impulses
        reaction_impulse_world_space = multiply_vectors_as_complex(reaction_impulse, self.normal)
        self.bodyA.rigidbody.apply_impulse_at_point( reaction_impulse_world_space, self.collision_point)
        self.bodyB.rigidbody.apply_impulse_at_point(-reaction_impulse_world_space, self.collision_point)

@dataclass
class CircleCollider(Collider):
    radius: float = 1

def get_collisions_circle_circle(bodyA: CircleCollider, bodyB: CircleCollider):
    total_radius = bodyA.radius + bodyB.radius
    posA: Vector2 = bodyA.position()
    posB: Vector2 = bodyB.position()
    distance = posA.distance_to(posB)

    if total_radius <= distance:
        return []
    else:
        return [Collision(
            bodyA = bodyA,
            bodyB = bodyB,
            collision_point = posA.lerp(posB, bodyA.radius / total_radius),
            penetration_distance = total_radius - distance,
            normal = (posB - posA) / distance
        )]
