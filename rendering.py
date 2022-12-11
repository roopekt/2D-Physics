from dataclasses import dataclass, field
from physics.bodies import *
from physics.PhysicsWorld import PhysicsWorld
from pygame import Color
from pygame.math import Vector2
import pygame
from utility import zero_vector_factory
import math

@dataclass
class Camera:
    position: Vector2 = field(default_factory=zero_vector_factory)
    height: float = 10

@dataclass
class RenderableBody:
    rigidbody: Rigidbody
    color: Color = field(default_factory=lambda: Color(0, 0, 0))

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
        if isinstance(collider, CircleCollider):
            self.draw_circle_collider(collider, color)
        elif isinstance(collider, RectangleCollider):
            self.draw_rectangle_collider(collider, color)
        else:
            raise Exception(f"Can't draw a {type(collider)}.")
    
    def draw_circle_collider(self, collider: CircleCollider, color: Color):
        collider_world_pos = collider.position()

        pygame.draw.circle(
            self.window,
            color,
            self.get_screen_position(collider_world_pos),
            collider.radius / self.get_scale())

        # extra cross
        orientation = collider.orientation()
        straight_angle = math.pi / 2.0
        beam_points = [Vector2(collider.radius, 0).rotate_rad(i * straight_angle + orientation) + collider_world_pos for i in range(4)] #world space
        beam_points = [self.get_screen_position(p) for p in beam_points] #screen space
        beam_color = Color(255, 255, 255) - color #negative color
        pygame.draw.line(self.window, beam_color, beam_points[0], beam_points[2])
        pygame.draw.line(self.window, beam_color, beam_points[1], beam_points[3])

    def draw_rectangle_collider(self, collider: RectangleCollider, color: Color):
        corners_world_space = collider.get_corners_counterclockwise()
        corners_screen_space = [self.get_screen_position(corner) for corner in corners_world_space]

        pygame.draw.polygon(
            self.window,
            color,
            corners_screen_space
        )

    def get_scale(self):
        return self.camera.height / self.window.get_height()

    def get_screen_position(self, world_position: Vector2):
        pos = (world_position - self.camera.position) / self.get_scale()
        pos.y = -pos.y
        pos += Vector2(self.window.get_width(), self.window.get_height()) / 2
        return pos
