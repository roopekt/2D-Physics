from dataclasses import dataclass, field
from pygame.math import Vector2
from utility import zero_vector_factory

@dataclass
class Collider:
    offset: Vector2 = field(default_factory=zero_vector_factory)
    angle_offset: float = 0
    parent: object = field(init=False) #Rigidbody (no type hint, because import would be circular)

    def position(self):
        return self.parent.position + self.offset.rotate_rad(self.parent.orientation)

    def orientation(self):
        return self.parent.orientation + self.angle_offset

    def get_collisions_with(self, other):
        if self.parent.is_static and other.parent.is_static:
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
