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
    return (n.dot(point_b - point_a))/n.dot(c)


def phit(point_a, t_hit, c):
    return point_a + (c * t_hit)


def reflection(c, n):
    norm_n = n.normalize()
    return c - (norm_n * c.dot(norm_n)) * 2

def collision(point_b, point_a, c, delta_time, direction, offset, smallest, t_hit):
    if delta_time >= t_hit >= 0:
        p_hit = phit(point_a, t_hit, c)
        if direction:
            if point_b.x <= p_hit.x <= point_b.x + offset:
                if smallest is None or t_hit < smallest[0]:
                    return True
        else:
            if point_b.y <= p_hit.y <= point_b.y + offset:
                if smallest is None or t_hit < smallest[0]:
                    return True
    return False


def paddle_collision(smallest, particle, delta_time, paddle):
    # List of all the normal vectors,
    # points on a line parallel to the normal vector
    # and the time that the particle will hit the line
    n_vectors = [Vector(0, 1), Vector(1, 0), Vector(1, 0)]
    point_list = [Point(paddle.position.x, paddle.position.y + PADDLE_HEIGHT),              # top point
                  Point(paddle.position.x + PADDLE_WIDTH, paddle.position.y),               # right point
                  paddle.position]                                                          # left point
    t_hit_list = [thit(n_vectors[0], point_list[0], particle.position, particle.motion),    # top time
                  thit(n_vectors[1], point_list[1], particle.position, particle.motion),    # right time
                  thit(n_vectors[2], point_list[2], particle.position, particle.motion)]    # left time
    # run through each time with the corresponding normal vector
    for n, t_hit in zip(n_vectors, t_hit_list):
        if delta_time >= t_hit >= 0:
            # Check if the particle will hit the line in this frame
            p_hit = phit(particle.position, t_hit, particle.motion)
            # If the normal vector for that time is pointing up its the top of the paddle
            if n == Vector(0, 1) and paddle.position.x <= p_hit.x <= paddle.position.x + PADDLE_WIDTH:
                if smallest is None or t_hit < smallest[0]:
                    return t_hit, n, paddle
            # If the normal vector is pointing to the right, its either of the sides
            elif n == Vector(1, 0) and paddle.position.y <= p_hit.y <= paddle.position.y + PADDLE_HEIGHT:
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
