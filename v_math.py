import math as m


# Finds time until point a intersects with line
def thit(n, point_b, point_a, c):
    return (n.dot(point_b - point_a)) / n.dot(c)


# finds point of contact on line
def phit(point_a, t_hit, c):
    return point_a + (c * t_hit)


# finds reflection vector
def reflection(c, n):
    norm_n = n.normalize()
    return c - (norm_n * c.dot(norm_n)) * 2


# Generic collision detection function
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


# Calculates new angle for ball based on where it makes contact to the paddle
def paddle_angle(base_angle, r_pos, p_hit, delta_angle, width):
    return base_angle + ((r_pos.x - p_hit.x) * (delta_angle / width))


# Describes a point on the window
class Point:
    def __init__(self, x, y):
        self.x = x  # X coordinate for point
        self.y = y  # Y coordinate for point

    # Overwrite operators
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __str__(self):
        return "Point(" + str(self.x) + ", " + str(self.y) + ")"

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)


# Describes a direction vector
class Vector:
    def __init__(self, x, y):
        self.x = x  # X direction for vector
        self.y = y  # Y direction for vector

    # Overwrite operators
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

    # Returns dot product of this vector and another
    def dot(self, other):
        return (self.x * other.x) + (self.y * other.y)

    # Normalizes the vector
    def normalize(self):
        v_len = m.sqrt(self.x * self.x + self.y * self.y)
        return Vector(self.x / v_len, self.y / v_len)
