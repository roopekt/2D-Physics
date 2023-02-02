import pygame
from pygame import Color
from pygame.math import Vector2
from rendering import *
from physics.bodies import *
from physics.PhysicsWorld import PhysicsWorld
from math import pi
from physics.contact_properties import *
from time import time

FPS = 60
world = RenderableWorld(
    bodies = [
        #region pile
        RenderableBody(
            Rigidbody(
                position = Vector2(0, 9),
                velocity = Vector2(0, 0),
                mass = 5,
                rotational_inertia = 5,
                colliders = [
                    CircleCollider(
                        radius = 1,
                        surface_material_name = "sticky"
                    )
                ]
            ),
            color = Color(0, 0, 255)
        ),
        RenderableBody(
            Rigidbody(
                position = Vector2(0, 7),
                mass = 5,
                rotational_inertia = 5,
                colliders = [
                    RectangleCollider(
                        size=Vector2(2, 2),
                        surface_material_name="bouncy slime"
                    )
                ]
            ),
            color = Color(255, 0, 0)
        ),
        RenderableBody(
            Rigidbody(
                position = Vector2(0, 5),
                velocity = Vector2(0, 0),
                mass = 5,
                rotational_inertia = 3,
                colliders = [
                    RectangleCollider(
                        size=Vector2(3, 3),
                        surface_material_name="bouncy slime"
                    )
                ]
            ),
            color = Color(0, 0, 255)
        ),
        RenderableBody(
            Rigidbody(
                position = Vector2(0, 2),
                velocity = Vector2(0, 0),
                mass = 1,
                rotational_inertia = 2,
                colliders = [
                    RectangleCollider(size=Vector2(1, 2))
                ]
            ),
            color = Color(255, 0, 0)
        ),
        #endregion

        #stick
        RenderableBody(
            Rigidbody(
                position = Vector2(3, 5),
                velocity = Vector2(0, 0),
                mass = 3,
                rotational_inertia = 10,
                colliders = [
                    RectangleCollider(size=Vector2(.2, 8))
                ]
            ),
            color = Color(128, 0, 0)
        ),

        #cross
        RenderableBody(
            Rigidbody(
                position = Vector2(-5, 6.2),
                orientation = .3,
                velocity = Vector2(20, 0),
                mass = 10,
                rotational_inertia = 50,
                colliders = [
                    RectangleCollider(
                        size = Vector2(1, 5),
                        surface_material_name = "default"
                    ),
                    RectangleCollider(
                        size = Vector2(5, 1),
                        surface_material_name = "default"
                    )
                ]
            ),
            color = Color(0, 255, 100)
        ),

        #extra ball
        RenderableBody(
            Rigidbody(
                position = Vector2(10, 1.8),
                orientation = -0.2,
                velocity = Vector2(0, 0),
                mass = 5,
                rotational_inertia = 5,
                colliders = [
                    CircleCollider(
                        radius = .8,
                    )
                ]
            ),
            color = Color(0, 0, 255)
        ),

        #floor
        RenderableBody(
            Rigidbody(
                position = Vector2(0, 0),
                colliders = [
                    RectangleCollider(
                        size = Vector2(200, 2)
                    )
                ],
                is_static = True
            )
        )
    ],
    camera = Camera(
        position = Vector2(2, 12/2),
        height = 12
    ),
    window = pygame.display.set_mode((1024, 512)),
    physics_world = PhysicsWorld(
        collision_iteration_count = 2,
        collision_velocity_iteration_count=2,
        air_density = 0.3
    )
)

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global should_be_running
            should_be_running = False

total_time = 0

should_be_running = True
clock = pygame.time.Clock()
while should_be_running:
    delta_time = clock.tick(FPS) / 1000 #we want delta_time in seconds
    delta_time = min(delta_time, 0.05)
    total_time += delta_time

    if (total_time > 2.5):
        pygame.image.save(world.window, f"capture/image.png")
        break

    handle_events()
    world.physics_world.advance(delta_time / 10)
    world.render()

pygame.quit()
