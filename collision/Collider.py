from pygame.math import Vector2
from dataclasses import dataclass, field
from Rigidbody import Rigidbody

@dataclass
class Collider:
    offset: Vector2 = Vector2.zero
    angle_offset: float = 0
    parent: Rigidbody = field(init=False)

    def position(self):
        return self.parent.position + self.offset.rotate_rad(self.parent.orientation)

    def orientation(self):
        return self.parent.orientation + self.angle_offset