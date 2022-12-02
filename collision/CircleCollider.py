from collision.Collider import Collider
from dataclasses import dataclass

@dataclass
class CircleCollider(Collider):
    radius: float = 1