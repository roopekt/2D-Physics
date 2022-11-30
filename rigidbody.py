from pygame.math import Vector2
from dataclasses import dataclass

@dataclass
class Rigidbody:
    position: Vector2
    velocity: Vector2
    mass: float #infinity should be supported
    orientation: float #an angle in radians from default orientation, counter clockwise 
    angular_velocity: float
    rotational_inertia: float #infinity should be supported

    def apply_impulse(self, impulse):
        self.velocity += impulse / self.mass

    def apply_angular_impulse(self, impulse):
        self.angular_velocity += impulse / self.rotational_inertia

    def apply_offcentered_impulse(self, impulse, offset):
        self.apply_impulse(impulse)
        self.apply_angular_impulse(offset.cross(impulse))