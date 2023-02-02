from pygame.math import Vector2
from .bodies import *
from dataclasses import dataclass
from itertools import permutations, combinations
from .contact_properties import ContactPropertyTable

CONTACT_PROPERTY_TABLE = ContactPropertyTable()

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
            normal = (posB - posA) / distance,
            contact_properties = get_contact_properties(bodyA, bodyB)
        )]

def get_collisions_rectangle_rectangle(bodyA: RectangleCollider, bodyB: RectangleCollider):
    if not are_enclosing_circles_colliding(bodyA, bodyB):
        return []

    collisions = get_collisions_rectangle_rectangle_naive(bodyA, bodyB)

    # Without this, cubes of same size on a floor can slide past each other,
    # because corners will be moving along the edges of the other collider.
    if len(collisions) >= 2:
        small_distance_squared = min(bodyA.get_smallest_edge_length(), bodyB.get_smallest_edge_length())**2 / 2
        for collisionA, collisionB in combinations(collisions, 2):
            are_close = collisionA.collision_point.distance_squared_to(collisionB.collision_point) < small_distance_squared
            similar_direction = collisionA.normal * collisionB.normal > 0.5
            if are_close and similar_direction:
                collisions.remove(collisionB)
                collisionA.normal = (collisionA.collision_point - collisionB.collision_point).normalize()

    for collision in collisions:
        collision.penetration_distance /= len(collisions) #to prevent position update from overshooting

    return collisions

def get_collisions_rectangle_rectangle_naive(bodyA: RectangleCollider, bodyB: RectangleCollider):
    @dataclass
    class EdgeCollision():
        edge: LineSegment
        penetration_distance: float

    collisions: list[Collision] = []
    for _bodyA, _bodyb in permutations((bodyA, bodyB)):
        for corner in _bodyA.get_corners_counterclockwise():

            corner_inside = True
            min_penetration_edge_collision = None
            for edge in _bodyb.get_edges_counterclockwise():
                distance_to_edge = project_perpendicular_to_axis(edge, corner)

                if distance_to_edge > 1e-4:
                    corner_inside = False
                    break
                elif min_penetration_edge_collision == None or -distance_to_edge < min_penetration_edge_collision.penetration_distance:#if we have a "better" edge
                    min_penetration_edge_collision = EdgeCollision(edge, -distance_to_edge)

            if corner_inside:
                collisions.append(Collision(
                    bodyA = _bodyA,
                    bodyB = _bodyb,
                    collision_point = corner,
                    penetration_distance = min_penetration_edge_collision.penetration_distance,
                    normal = min_penetration_edge_collision.edge.normal(),
                    contact_properties = get_contact_properties(bodyA, bodyB)
                ))

    return collisions

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
            normal = -circle_normal,
            contact_properties = get_contact_properties(rectangle, circle)
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
            normal = (circle_pos - corner) / distance,
            contact_properties = get_contact_properties(rectangle, circle)
        )]

def are_enclosing_circles_colliding(bodyA: Collider, bodyB: Collider):
    total_radius = bodyA.encircling_radius() + bodyB.encircling_radius()
    distance_squared = bodyA.position().distance_squared_to(bodyB.position())
    return distance_squared < total_radius**2

def project_perpendicular_to_axis(axis: LineSegment, point: Vector2):
    return -axis.tangent().cross(point - axis.pointA)

def get_contact_properties(bodyA: Collider, bodyB: Collider):
    return CONTACT_PROPERTY_TABLE.get_contact_properties(bodyA.surface_material_name, bodyB.surface_material_name)
