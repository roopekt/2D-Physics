import pygame
from pygame import Color, Vector2
from rendering import *
from physics.bodies import *
from physics.PhysicsWorld import PhysicsWorld
from math import pi

FPS = 60
world = RenderableWorld(
    bodies = [
        RenderableBody(
            Rigidbody(
                position = Vector2(0, 0),
                orientation = 0.5,
                angular_velocity = 0,
                mass = 10,
                rotational_inertia = 10,
                colliders = [
                    RectangleCollider(
                        size = Vector2(2, 2),
                        elasticity = 0.5
                    )
                ]
            ),
            color = Color(255, 0, 0)
        ),
        RenderableBody(
            Rigidbody(
                position = Vector2(0, -10),
                colliders = [
                    RectangleCollider(
                        size = Vector2(15, 1)
                    )
                ],
                is_static = True
            )
        )
    ],
    camera = Camera(
        position = Vector2(0, 0),
        height = 50
    ),
    physics_world = PhysicsWorld(
        collision_iteration_count = 5
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
