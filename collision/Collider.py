from pygame.math import Vector2
from dataclasses import dataclass, field
from Rigidbody import Rigidbody
from utility import zero_vector_factory

@dataclass
class Collider:
    offset: Vector2 = field(default_factory=zero_vector_factory)
    angle_offset: float = 0
    parent: Rigidbody = field(init=False)

    def position(self):
        return self.parent.position + self.offset.rotate_rad(self.parent.orientation)

    def orientation(self):
        return self.parent.orientation + self.angle_offset