from pygame import Vector2

def zero_vector_factory():
    return Vector2(0.0, 0.0)

def get_tangent(normal: Vector2): #rotate by 90 degrees clockwise
    return Vector2(normal.y, -normal.x)

def vector_to_complex(v: Vector2):
    return complex(v.x, v.y)

def complex_to_vector(z: complex):
    return Vector2(z.real, z.imag)

def multiply_vectors_as_complex(vecA: Vector2, vecB: Vector2):
    return complex_to_vector(vector_to_complex(vecA) * vector_to_complex(vecB))

def divide_vectors_as_complex(vecA: Vector2, vecB: Vector2):
    return complex_to_vector(vector_to_complex(vecA) / vector_to_complex(vecB))