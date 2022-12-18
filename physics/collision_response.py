from pygame.math import Vector2
from math_helpers import *
import math
from .bodies import Collision
from statistics import mean
import numpy as np
from math_helpers import get_tangent

def update_velocities(collision: Collision):
    tangent = get_tangent(collision.normal)
    relative_velocity: Vector2 = (collision.bodyB.rigidbody.velocity_at_point(collision.collision_point)
                                - collision.bodyA.rigidbody.velocity_at_point(collision.collision_point))
    relative_velocity = divide_vectors_as_complex(relative_velocity, tangent) #transform into collision space (rotate so that y is in the direction of the normal)

    if relative_velocity.y > 0.0: #if moving away from each other
        return

    #reaction impulse assuming rest friction is possible
    target_velocity_change = Vector2(-relative_velocity.x, -(1 + collision.contact_properties.elasticity) * relative_velocity.y)
    reaction_impulse = get_required_impulse_for_velocity_change(target_velocity_change, collision)

    #is rest friction possible?
    max_rest_friction = collision.contact_properties.rest_friction_coefficient * abs(reaction_impulse.y)
    rest_friction_possible = abs(reaction_impulse.x) < max_rest_friction

    #dynamic friction
    if not rest_friction_possible:
        reaction_impulse = get_required_impulse_for_velocity_change_dynamic_friction(target_velocity_change.y, collision, sign(reaction_impulse.x))

    #apply the impulses
    reaction_impulse_world_space = multiply_vectors_as_complex(reaction_impulse, tangent)
    collision.bodyA.rigidbody.apply_impulse_at_point( reaction_impulse_world_space, collision.collision_point)
    collision.bodyB.rigidbody.apply_impulse_at_point(-reaction_impulse_world_space, collision.collision_point)

def update_positions(collision: Collision):
    massA = collision.bodyA.rigidbody.mass
    massB = collision.bodyB.rigidbody.mass
    total_mass = massA + massB

    nan_to_one = lambda x: 1.0 if math.isnan(x) else x #to make infinite masses work properly
    contributionA = nan_to_one(massB / total_mass) #just switching A and B isn't physically accurate, but nor is the idea of this whole function. good enough
    contributionB = nan_to_one(massA / total_mass)

    penetration_distance = collision.penetration_distance + 0.002 # a small extra is added so that we don't redetect the collision

    collision.bodyA.rigidbody.position -= collision.normal * penetration_distance * contributionA
    collision.bodyB.rigidbody.position += collision.normal * penetration_distance * contributionB

#in collision space
def get_required_impulse_for_velocity_change(target_velocity_change: Vector2, collision: Collision) -> Vector2:
    response_to_dx = get_delta_velocity_collision_space(Vector2(1, 0), collision)
    response_to_dy = get_delta_velocity_collision_space(Vector2(0, 1), collision)

    matrix = np.array([[response_to_dx.x, response_to_dy.x],
                       [response_to_dx.y, response_to_dy.y]])
    target = np.array([-target_velocity_change.x, -target_velocity_change.y])
    stopping_impulse = np.linalg.solve(matrix, target)

    return Vector2(stopping_impulse[0], stopping_impulse[1])

#in collision space
def get_required_impulse_for_velocity_change_dynamic_friction(target_velocity_change_along_normal: float, collision: Collision, dynamic_friction_sign: float) -> Vector2:
    dynamic_friction_coefficient = dynamic_friction_sign * collision.contact_properties.dynamic_friction_coefficient

    test_impulse = Vector2(1, dynamic_friction_coefficient)
    response_to_test = get_delta_velocity_collision_space(test_impulse, collision)

    multiplyer = target_velocity_change_along_normal / response_to_test.y
    return multiplyer * test_impulse

def get_delta_velocity_collision_space(impulse: Vector2, collision: Collision):
    tangent = get_tangent(collision.normal)
    impulse = multiply_vectors_as_complex(impulse, tangent)
    global_space_reaction = (collision.bodyB.rigidbody.get_delta_velocity(impulse, collision.collision_point)
                           - collision.bodyA.rigidbody.get_delta_velocity(impulse, collision.collision_point))
    return divide_vectors_as_complex(global_space_reaction, tangent)