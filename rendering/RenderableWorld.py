from dataclasses import dataclass, field
from rendering.RenderableBody import RenderableBody
from rendering.Camera import Camera
from collision.Collider import Collider
from PhysicsWorld import PhysicsWorld
from pygame import Color
from pygame.math import Vector2
import pygame

@dataclass
class RenderableWorld:
    bodies: list[RenderableBody] = field(default_factory=list)
    camera: Camera = field(default_factory=lambda: Camera())
    background_color: Color = field(default_factory=lambda: Color(255, 255, 255))
    window: pygame.Surface = field(default_factory=lambda: pygame.display.set_mode((640, 480), pygame.RESIZABLE))
    physics_world: PhysicsWorld = field(default_factory=lambda: PhysicsWorld())

    def __post_init__(self):
        self.physics_world.bodies += [body.rigidbody for body in self.bodies]

    def render(self):
        self.window.fill(self.background_color)

        for body in self.bodies:
            for collider in body.rigidbody.colliders:
                self.draw_collider(collider, body.color)

        pygame.display.flip()

    def draw_collider(self, collider: Collider, color: Color):
        scale = self.camera.height / self.window.get_height()
        position = (collider.position() - self.camera.position) / scale
        position.y = -position.y
        position += Vector2(self.window.get_width(), self.window.get_height()) / 2

        #temporary
        pygame.draw.circle(
            self.window,
            color,
            position,
            collider.radius / scale)
