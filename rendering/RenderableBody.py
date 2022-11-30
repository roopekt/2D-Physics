from dataclasses import dataclass, field
from Rigidbody import Rigidbody
from pygame import Color

@dataclass
class RenderableBody:
    rigidbody: Rigidbody
    color: Color = field(default_factory=lambda: Color(0, 0, 0))