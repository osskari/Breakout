import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)


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


class Paddle:
    def __init__(self, position, speed):
        self.position = position
        self.speed = speed
        self.direction = [False, False]

    def draw(self, p_color):
        glColor3f(p_color[0], p_color[1], p_color[2])

        glPushMatrix()

        glTranslate(self.position.x, self.position.y, 0)

        glBegin(GL_TRIANGLES)
        glVertex2f(-30, -10)
        glVertex2f(30, -10)
        glVertex2f(-30, 10)

        glVertex2f(-30, 10)
        glVertex2f(30, -10)
        glVertex2f(30, 10)
        glEnd()

        glPopMatrix()

    def update(self, delta_time):
        if self.direction[0]:
            self.position -= Vector(self.speed, 0) * delta_time
        if self.direction[1]:
            self.position += Vector(self.speed, 0) * delta_time


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
