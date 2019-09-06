import math as m

from globals import *
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
    motion = Vector(-m.sin(angle * m.pi / 180.0), m.cos(angle * m.pi / 180.0))

    return motion * speed


def phit(point_a, t_hit, c):
    return point_a + c * t_hit


def thit(n, point_b, point_a, c):
    return (n.dot(point_b - point_a))/n.dot(c)


def reflection(c, n):
    return c - n*(((c.dot(n)) * 2)/n.dot(n))


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def dotprod(self, other):
        return self.x * other.x + self.y * other.y


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

