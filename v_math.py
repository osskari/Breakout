import math as m
from objects import Vector

# a place for vector math and shit


def move_player(direction, speed):
    if direction == "LEFT":
        motion = speed
    elif direction == "RIGHT":
        motion = -speed
    else:
        motion = 0

    return motion


def update_ball(angle, speed):

    acceleration = Vector((-m.sin(angle * m.pi / 180.0), m.cos(angle * m.pi / 180.0)))
    return acceleration * speed


def reflection(Vector):
    pass