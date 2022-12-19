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
        #region cubes
        RenderableBody(
            Rigidbody(
                position = Vector2(-10, 30),
                velocity = Vector2(0, 0),
                mass = 5,
                rotational_inertia = 5,
                colliders = [
                    RectangleCollider()
                ]
            ),
            color = Color(255, 0, 0)
        ),
        RenderableBody(
            Rigidbody(
                position = Vector2(10, 30),
                velocity = Vector2(0, 0),
                mass = 5,
                rotational_inertia = 5,
                colliders = [
                    RectangleCollider()
                ]
            ),
            color = Color(255, 0, 0)
        ),
        #endregion

        #red ball
        RenderableBody(
            Rigidbody(
                position = Vector2(-15, 40),
                velocity = Vector2(-15, 2),
                mass = 10,
                rotational_inertia = 10,
                colliders = [
                    CircleCollider(
                        surface_material_name = "default",
                        radius = 1.5
                    )
                ]
            ),
            color = Color(255, 0, 0)
        ),

        #super ball
        RenderableBody(
            Rigidbody(
                position = Vector2(0, 40),
                velocity = Vector2(50, 0),
                mass = 20,
                rotational_inertia = 20,
                colliders = [
                    CircleCollider(
                        surface_material_name = "bouncy slime",
                        radius = 2
                    )
                ]
            ),
            color = Color(0, 255, 0)
        ),

        #cross
        RenderableBody(
            Rigidbody(
                position = Vector2(0, 25),
                velocity = Vector2(0, 0),
                mass = 10,
                rotational_inertia = 20,
                colliders = [
                    RectangleCollider(
                        size = Vector2(1, 5),
                        surface_material_name = "frictionless"
                    ),
                    RectangleCollider(
                        size = Vector2(5, 1),
                        surface_material_name = "frictionless"
                    )
                ]
            ),
            color = Color(0, 200, 255)
        ),

        #region walls:
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
        ),
        RenderableBody(
            Rigidbody(
                position = Vector2(-30, 100),
                colliders = [
                    RectangleCollider(
                        size = Vector2(2, 200),
                        surface_material_name = "bouncy slime"
                    )
                ],
                is_static = True
            ),
            color = Color(0, 128, 0)
        ),
        RenderableBody(
            Rigidbody(
                position = Vector2(30, 100),
                colliders = [
                    RectangleCollider(
                        size = Vector2(2, 200),
                        surface_material_name = "bouncy slime"
                    )
                ],
                is_static = True
            ),
            color = Color(0, 128, 0)
        ),
        RenderableBody(
            Rigidbody(
                position = Vector2(0, 20),
                orientation = 0.5,
                colliders = [
                    RectangleCollider(
                        size = Vector2(20, 1.5)
                    )
                ],
                is_static = True
            )
        )
        #endregion
    ],
    camera = Camera(
        position = Vector2(0, 25),
        height = 50
    ),
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
            
last_frame_time = time()
frame_index = 0

should_be_running = True
clock = pygame.time.Clock()
while should_be_running:
    delta_time = clock.tick(FPS) / 1000 #we want delta_time in seconds
    delta_time = min(delta_time, 0.05)

    if time() - last_frame_time > 0.2:
        pygame.image.save(world.window, f"capture/frame{frame_index}.png")
        frame_index += 1
        last_frame_time = time()

    if frame_index > 10:
        break

    handle_events()
    world.physics_world.advance(delta_time)
    world.render()

    bodyA = world.physics_world.bodies[0]

pygame.quit()
