class Point:
    def __init__(self, position):
        self.position = position

    def __add__(self, other):
        new_position = (self.position[0] + other.position[0], self.position[1] + other.position[1])
        return Point(new_position)


class Vector:
    def __init__(self, motion):
        self.motion = motion

    def __add__(self, other):
        new_vector = (self.motion[0] + other.motion[0], self.motion[1] + other.motion[1])
        return Vector(new_vector)

    def __mul__(self, other):
        new_vector = (self.motion[0] * other, self.motion[1] * other)
        return Vector(new_vector)


class Paddle:
    def __init__(self):
        self.position = 0
        self.motion = 0
        self.speed = 0

    def draw(self):
        pass

    def update(self):
        pass


class Ball:
    def __init__(self):
        self.position = 0
        self.motion = 0
        self.speed = 0
        self.angle = 0
        self.in_play = False

    def draw(self):
        # if not in play attach to top middle of paddle
        pass

    def update(self):
        pass


class Brick:
    def __init__(self):
        self.hits = 0

    def draw(self):
        # if hits == 0: don't draw or collide
        # different colour based on hit count
        pass

    def update(self):
        pass
