from pygame.math import Vector2
from .bodies import *

def get_collisions_between(bodyA: Collider, bodyB: Collider):
    if bodyA.rigidbody.is_static and bodyB.rigidbody.is_static:
        return []

    if isinstance(bodyA, CircleCollider) and isinstance(bodyB, CircleCollider):
        return get_collisions_circle_circle(bodyA, bodyB)
    else:
        raise Exception(f"Can't check collision between a {type(bodyA)} and a {type(bodyB)}.")

def get_collisions_circle_circle(bodyA: CircleCollider, bodyB: CircleCollider):
    total_radius = bodyA.radius + bodyB.radius
    posA: Vector2 = bodyA.position()
    posB: Vector2 = bodyB.position()
    distance = posA.distance_to(posB)

    if total_radius < distance:
        return []
    else:
        return [Collision(
            bodyA = bodyA,
            bodyB = bodyB,
            collision_point = posA.lerp(posB, bodyA.radius / total_radius),
            penetration_distance = total_radius - distance,
            normal = (posB - posA) / distance
        )]