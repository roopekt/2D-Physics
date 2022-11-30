from dataclasses import dataclass, field
from pygame.math import Vector2
from utility import zero_vector_factory

@dataclass
class Camera:
    position: Vector2 = field(default_factory=zero_vector_factory)
    height: float = 10