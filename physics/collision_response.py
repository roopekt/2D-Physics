from pygame.math import Vector2
from utility import divide_vectors_as_complex, multiply_vectors_as_complex, get_tangent
import math
from .bodies import Collision

def update_velocities(collision: Collision):
    tangent = get_tangent(collision.normal)
    relative_velocity: Vector2 = (collision.bodyB.rigidbody.velocity_at_point(collision.collision_point)
                                - collision.bodyA.rigidbody.velocity_at_point(collision.collision_point))
    relative_velocity = divide_vectors_as_complex(relative_velocity, tangent) #rotate so that y is in the direction of the normal
    reaction_impulse = Vector2(0.0)

    if relative_velocity.y > 0.0:
        return

    #bounce
    velocity_change_for_unit_impulse = (collision.bodyA.rigidbody.apply_test_impulse( collision.normal, collision.collision_point)
                                        + collision.bodyB.rigidbody.apply_test_impulse(-collision.normal, collision.collision_point))
    elasticity = max(collision.bodyA.elasticity, collision.bodyB.elasticity)
    target_velocity_change = (1 + elasticity) * relative_velocity.y
    reaction_impulse.y = target_velocity_change / velocity_change_for_unit_impulse

    #TODO: friction


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

    collision.bodyA.rigidbody.position -= collision.normal * collision.penetration_distance * contributionA
    collision.bodyB.rigidbody.position += collision.normal * collision.penetration_distance * contributionB