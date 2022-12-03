from pygame.math import Vector2
from dataclasses import dataclass, field
from .collision import Collider
from utility import zero_vector_factory

@dataclass
class Rigidbody:
    position: Vector2 = field(default_factory=zero_vector_factory)
    velocity: Vector2 = field(default_factory=zero_vector_factory)
    mass: float = 1
    orientation: float = 0 #an angle in radians from the default orientation, counter clockwise 
    angular_velocity: float = 0
    rotational_inertia: float = 1
    colliders: list[Collider] = field(default_factory=list)
    is_static: bool = False

    def __post_init__(self):
        for collider in self.colliders:
            collider.parent = self

        if self.is_static:
            self.mass = float('inf')
            self.rotational_inertia = float('inf')

    def apply_impulse(self, impulse):
        self.velocity += impulse / self.mass

    def apply_angular_impulse(self, impulse):
        self.angular_velocity += impulse / self.rotational_inertia

    def apply_offcentered_impulse(self, impulse, offset):
        self.apply_impulse(impulse)
        self.apply_angular_impulse(offset.cross(impulse))