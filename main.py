import pygame
from pygame import Color
from pygame.math import Vector2
from rendering import *
from physics.Rigidbody import Rigidbody
from physics.collision import CircleCollider

FPS = 60
world = RenderableWorld(
    bodies = [
        RenderableBody(
            Rigidbody(
                position = Vector2(0, 20),
                angular_velocity = 0,
                mass = 10,
                colliders = [
                    CircleCollider(
                        elasticity = 1.0
                    )
                ]
            ),
            color = Color(255, 0, 0)
        ),
        RenderableBody(
            Rigidbody(
                position = Vector2(0, 15),
                angular_velocity = 0,
                colliders = [
                    CircleCollider(
                        elasticity = 1.0
                    )
                ]
            )
        ),
        RenderableBody(
            Rigidbody(
                position = Vector2(0, -10),
                colliders = [
                    CircleCollider(radius=2)
                ],
                is_static = True
            )
        )
    ],
    camera = Camera(
        position = Vector2(0, 0),
        height = 50
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
    delta_time = clock.tick(FPS) / 1000 #we want delta_time in seconds

    handle_events()
    world.physics_world.advance(delta_time)
    world.render()

pygame.quit()
