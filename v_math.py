import math as m

from globals import *


def thit(n, point_b, point_a, c):
    return (n.dot(point_b - point_a))/n.dot(c)


def phit(point_a, t_hit, c):
    return point_a + (c * t_hit)


def reflection(c, n):
    norm_n = n.normalize()
    return c - (norm_n * c.dot(norm_n)) * 2


def collision(point_b, point_a, c, delta_time, direction, offset, smallest, t_hit):
    # if time of collision is within the next frame calculate point of contact
    if delta_time >= t_hit >= 0:
        p_hit = phit(point_a, t_hit, c)
        # horizontal and vertical
        if direction:
            # if point of contact is within the boundaries of the model
            if point_b.x <= p_hit.x <= point_b.x + offset:
                # if this collision happens before the current closest collision, replace it
                if smallest is None or t_hit < smallest[0]:
                    return True
        else:
            if point_b.y <= p_hit.y <= point_b.y + offset:
                if smallest is None or t_hit < smallest[0]:
                    return True
    # false if any of the statements are false
    return False


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __str__(self):
        return "Point(" + str(self.x) + ", " + str(self.y) + ")"

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)


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
