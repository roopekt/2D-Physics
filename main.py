import pygame
from pygame import Color
from pygame.math import Vector2
from rendering.RenderableWorld import RenderableWorld
from rendering.RenderableBody import RenderableBody
from rendering.Camera import Camera
from Rigidbody import Rigidbody
from collision.CircleCollider import CircleCollider

FPS = 60
world = RenderableWorld(
    bodies = [
        RenderableBody(
            Rigidbody(
                position = Vector2(0, 0),
                colliders = [
                    CircleCollider()
                ]
            )
        )
    ],
    camera = Camera(
        position = Vector2(0, 0),
        height = 20
    )
)

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global should_be_running
            should_be_running = False

should_be_running = True
clock = pygame.time.Clock()
while should_be_running:
    delta_time = clock.tick(FPS)

    handle_events()
    world.render()

pygame.quit()
