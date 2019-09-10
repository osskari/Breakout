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


def thit(n, point_b, point_a, c):
    bsuba = point_b - point_a
    over = n.dot(bsuba)
    under = n.dot(c)
    # return (n.dot(point_b - point_a))/n.dot(c)
    return over / under


def phit(point_a, t_hit, c):
    return point_a + (c * t_hit)


def reflection(c, n):
    norm_n = n.normalize()
    return c - (norm_n * c.dot(norm_n)) * 2


def collision(smallest, normal, point, particle, delta_time, x_offset, y_offset):
    t_hit = thit(normal, Point(point.position.x + x_offset, point.position.y + y_offset), particle.position,
                 particle.motion)
    if delta_time >= t_hit >= 0:
        p_hit = phit(particle.position, t_hit, particle.motion)
        if point.position.x <= p_hit.x <= point.position.x + BRICK_WIDTH:
            if smallest is None or t_hit < smallest[0]:
                return t_hit, normal, point
    return smallest


def paddle_collision(smallest, particle, delta_time, paddle):
    n_vectors = [Vector(0, 1), Vector(1, 0), Vector(-1, 0)]
    point_list = [Point(paddle.position.x, paddle.position.y + PADDLE_HEIGHT),          # top
                  Point(paddle.position.x + PADDLE_WIDTH, paddle.position.y),           # right
                  Point(paddle.position.x, paddle.position.y + PADDLE_HEIGHT // 2)]     # left
    t_hit_list = [thit(n_vectors[0], point_list[0], particle.position, particle.motion),    # top
                  thit(n_vectors[1], point_list[1], particle.position, particle.motion),    # right
                  thit(n_vectors[2], point_list[2], particle.position, particle.motion)]    # left
    # top
    for n, t_hit in zip(n_vectors, t_hit_list):
        if delta_time >= t_hit >= 0:
            p_hit = phit(particle.position, t_hit, particle.motion)
            if n == Vector(0, 1) and paddle.position.x <= p_hit.x <= paddle.position.x + PADDLE_WIDTH:
                if smallest is None or t_hit < smallest[0]:
                    return t_hit, n, paddle
            elif (n == Vector(1, 0) or n == Vector(-1, 0)) and paddle.position.y <= p_hit.y <= paddle.position.y + PADDLE_HEIGHT:
                if smallest is None or t_hit < smallest[0]:
                    return t_hit, n, paddle

    return smallest


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __str__(self):
        return "Point(" + str(self.x) + ", " + str(self.y) + ")"

    def y_axis_ge(self, other):
        return self.y >= other.y

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def x_axis_ge(self, other):
        return self.x >= other.x

    def is_between_x(self, left, right):
        return left <= self.x <= right

    def is_between_y(self, bottom, top):
        return bottom <= self.y <= top


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

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "Vector(" + str(self.x) + ", " + str(self.y) + ")"

    def dot(self, other):
        return (self.x * other.x) + (self.y * other.y)

    def normalize(self):
        v_len = m.sqrt(self.x * self.x + self.y * self.y)
        return Vector(self.x / v_len, self.y / v_len)
