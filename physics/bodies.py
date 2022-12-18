from pygame.math import Vector2
from dataclasses import dataclass, field
from math_helpers import zero_vector_factory, get_tangent
from abc import ABC, abstractmethod
from .contact_properties import ContactProperties

@dataclass
class Rigidbody:
    position: Vector2 = field(default_factory=zero_vector_factory)
    velocity: Vector2 = field(default_factory=zero_vector_factory)
    mass: float = 1
    orientation: float = 0 #an angle in radians from the default orientation, counter clockwise 
    angular_velocity: float = 0
    rotational_inertia: float = 1
    colliders: list = field(default_factory=list)
    is_static: bool = False
    drag_coefficient: float = 0.8
    angular_drag_coefficient: float = 0.2

    def __post_init__(self):
        for collider in self.colliders:
            collider.rigidbody = self

        if self.is_static:
            self.mass = float('inf')
            self.rotational_inertia = float('inf')

    def apply_impulse(self, impulse):
        self.velocity += impulse / self.mass

    def apply_angular_impulse(self, impulse):
        self.angular_velocity += impulse / self.rotational_inertia

    def apply_impulse_at_point(self, impulse, point):
        offset = self.get_offset(point)
        self.apply_impulse(impulse)
        self.apply_angular_impulse(offset.cross(impulse))

    def velocity_at_point(self, point: Vector2): #point is in world space
        offset = self.get_offset(point)
        return self.velocity - get_tangent(offset) * self.angular_velocity


    def apply_test_impulse(self, unit_impulse: Vector2, point: Vector2): #how much the velocity of point (world space) would change along the unit_impulse vector if said impulse was applied at the point?
        # code assumes unit_impulse is a unit vector

        linear_reaction = 1 / self.mass # (impulse / mass) * impulse.normalize()

        # rotational_reaction = offset x impulse / rotational_inertia (change of angular velocity)
        # * offset x impulse.normalize()
        offset = self.get_offset(point)
        rotational_reaction = offset.cross(unit_impulse)**2 / self.rotational_inertia

        return linear_reaction + rotational_reaction

    def get_offset(self, world_space_point): #vector from this object to world_space_point
        return world_space_point - self.position

@dataclass
class LineSegment:
    pointA: Vector2
    pointB: Vector2

    def tangent(self):
        return (self.pointB - self.pointA).normalize()

    def normal(self):
        return -get_tangent(self.tangent())

@dataclass
class Collider(ABC):
    offset: Vector2 = field(default_factory=zero_vector_factory)
    angle_offset: float = 0
    surface_material_name: str = "default"
    rigidbody: Rigidbody = field(init=False)

    def position(self):
        return self.rigidbody.position + self.offset.rotate_rad(self.rigidbody.orientation)

    def orientation(self):
        return self.rigidbody.orientation + self.angle_offset

    @abstractmethod
    def encircling_radius(self):
        pass

@dataclass
class CircleCollider(Collider):
    radius: float = 1

    def encircling_radius(self):
        return self.radius

@dataclass
class RectangleCollider(Collider):
    size: Vector2 = field(default_factory=lambda: Vector2(2, 1.5))

    def encircling_radius(self):
        return self.size.magnitude() / 2

    def get_corners_counterclockwise(self) -> list[Vector2]:
        position = self.position()
        orientation = self.orientation()

        corners = [
            Vector2( .5,  .5),
            Vector2(-.5,  .5),
            Vector2(-.5, -.5),
            Vector2( .5, -.5)
        ]
        corners = [corner.elementwise() * self.size for corner in corners] #scale
        corners = [corner.rotate_rad(orientation) for corner in corners] #rotate
        corners = [corner + position for corner in corners] #translate

        return corners

    def get_edges_counterclockwise(self) -> list[LineSegment]:
        corners = self.get_corners_counterclockwise()
        return [LineSegment(corners[i], corners[(i+1) % 4]) for i in range(4)]

@dataclass
class Collision:
    bodyA: Collider
    bodyB: Collider
    collision_point: Vector2 #world space
    penetration_distance: float
    normal: Vector2 #surface normal of bodyA (outwards pointing) at collision_point
    contact_properties: ContactProperties
