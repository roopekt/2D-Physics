from pygame.math import Vector2
from dataclasses import dataclass
from Collider import Collider

@dataclass
class Collision:
    bodyA: Collider
    bodyB: Collider
    collision_point: Vector2 #world space
    penetration_distance: float
    normal: Vector2 #surface normal of bodyA (outwards pointing) at collision_point