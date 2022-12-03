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