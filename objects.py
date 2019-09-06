import math as m

import pygame
from pygame.locals import *

from globals import *
from v_math import *

from OpenGL.GL import *
from OpenGL.GLU import *


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
        if self.direction[PADDLE_LEFT] and self.position.x - 30 > 0:
            self.position -= Vector(self.speed, 0) * delta_time
        if self.direction[PADDLE_RIGHT] and self.position.x + 30 < WINDOW_WIDTH:
            self.position += Vector(self.speed, 0) * delta_time


class Ball:
    def __init__(self, position, speed):
        self.position = position
        self.motion = 0
        self.speed = speed
        self.angle = 45
        self.in_play = False
        self.radius = 5

    def draw(self, b_color):
        glColor3f(b_color[0], b_color[1], b_color[2])

        glPushMatrix()

        glTranslate(self.position.x, self.position.y, 0)

        glPointSize(4)

        glBegin(GL_POINTS)
        glVertex2f(0, 0)
        glEnd()

        glPopMatrix()

    def update(self, delta_time):
        # if not in play attach to top middle of paddle
        if self.in_play:
            # self.motion = Vector(-m.sin(self.angle * m.pi / 180.0), m.cos(self.angle * m.pi / 180.0)) * self.speed
            self.motion = update_ball(self.angle, self.speed)
        else:
            self.motion = Vector(0, 0)
        self.position += self.motion * delta_time


class Brick:
    def __init__(self):
        self.hits = 0

    def draw(self):
        # if hits == 0: don't draw or collide
        # different colour based on hit count
        pass

    def update(self):
        pass
