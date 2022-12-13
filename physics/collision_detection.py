from pygame.math import Vector2
from .bodies import *
from dataclasses import dataclass

def get_collisions_between(bodyA: Collider, bodyB: Collider):
    if bodyA.rigidbody.is_static and bodyB.rigidbody.is_static:
        return []

    if isinstance(bodyA, CircleCollider) and isinstance(bodyB, CircleCollider):
        return get_collisions_circle_circle(bodyA, bodyB)
    elif isinstance(bodyA, CircleCollider) and isinstance(bodyB, RectangleCollider):
        return get_collisions_rectangle_circle(bodyB, bodyA)
    elif isinstance(bodyA, RectangleCollider) and isinstance(bodyB, CircleCollider):
        return get_collisions_rectangle_circle(bodyA, bodyB)
    elif isinstance(bodyA, RectangleCollider) and isinstance(bodyB, RectangleCollider):
        return get_collisions_rectangle_rectangle(bodyA, bodyB)
    else:
        raise Exception(f"Can't check for collisions between a {type(bodyA)} and a {type(bodyB)}.")

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

def get_collisions_rectangle_rectangle(bodyA: RectangleCollider, bodyB: RectangleCollider):
    pass

def get_collisions_rectangle_circle(rectangle: RectangleCollider, circle: CircleCollider):
    if not are_enclosing_circles_colliding(rectangle, circle):
        return []

    edges = rectangle.get_edges_counterclockwise()
    circle_pos = circle.position()

    @dataclass
    class EdgeCollision():
        edge: LineSegment
        distance: float

    edge_collisions: list[EdgeCollision] = []
    for edge in edges:
        dist_to_edge = project_perpendicular_to_axis(edge, circle_pos)
        if 0 <= dist_to_edge <= circle.radius:
            edge_collisions.append(EdgeCollision(edge, dist_to_edge))
        elif dist_to_edge > circle.radius:
            return []

        if len(edge_collisions) >= 2:
            break

    if len(edge_collisions) == 0:
        return []
    elif len(edge_collisions) == 1:
        edge = edge_collisions[0].edge
        circle_normal = edge.normal() #from circle towards the edge
        distance_to_edge = edge_collisions[0].distance

        return [Collision(
            bodyA = rectangle,
            bodyB = circle,
            collision_point = circle_pos + circle_normal * circle.radius,
            penetration_distance = circle.radius - distance_to_edge,
            normal = -circle_normal
        )]
    elif len(edge_collisions) == 2:
        corner: Vector2 = edge_collisions[0].edge.pointB if edge_collisions[0].edge.pointB is edge_collisions[1].edge.pointA else edge_collisions[0].edge.pointA
        distance = circle_pos.distance_to(corner)

        if distance > circle.radius:
            return []

        return [Collision(
            bodyA = rectangle,
            bodyB = circle,
            collision_point = corner,
            penetration_distance = circle.radius - distance,
            normal = (circle_pos - corner) / distance
        )]

def are_enclosing_circles_colliding(bodyA: Collider, bodyB: Collider):
    total_radius = bodyA.encircling_radius() + bodyB.encircling_radius()
    distance_squared = bodyA.position().distance_squared_to(bodyB.position())
    return distance_squared < total_radius**2

def project_perpendicular_to_axis(axis: LineSegment, point: Vector2):
    return -axis.tangent().cross(point - axis.pointA)
