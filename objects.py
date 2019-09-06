import math as m

import pygame
from pygame.locals import *

from globals import *
from v_math import *

from OpenGL.GL import *
from OpenGL.GLU import *


class Paddle:
    def __init__(self, position, speed, ball):
        self.position = position
        self.motion = Vector(0, 0)
        self.speed = speed
        self.direction = [False, False]
        self.ball = ball

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
            self.motion = Vector(self.speed, 0)
            self.position -= self.motion * delta_time
        if self.direction[PADDLE_RIGHT] and self.position.x + 30 < WINDOW_WIDTH:
            self.motion = Vector(self.speed, 0)
            self.position += self.motion * delta_time


class Ball:
    def __init__(self, position, speed):
        self.position = position
        self.motion = Vector(0, 0)
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

    def update(self, delta_time, paddle_position):
        # if not in play attach to top middle of paddle
        if self.in_play:
            if self.motion == Vector(0, 0):
                self.motion = Vector(-m.sin(self.angle * m.pi / 180.0), m.cos(self.angle * m.pi / 180.0)) * self.speed
            self.collision(delta_time)
        else:
            self.motion = Vector(0, 0)
            self.position = paddle_position
        self.position += self.motion * delta_time

    def collision(self, delta_time):
        window_points = [Point(0, 0), Point(WINDOW_WIDTH, 0), Point(WINDOW_WIDTH, 0),
                         Point(WINDOW_WIDTH, WINDOW_HEIGHT)]
        window_n = (Vector(-1, 0), Vector(1, 0), Vector(0, -1), Vector(0, 1))
        for p, n in zip(window_points, window_n):
            t_hit = thit(n, p, self.position, self.motion * delta_time)
            if 1 >= t_hit >= 0:
                self.motion = reflection(self.motion, n)


class Brick:
    def __init__(self):
        self.hits = 0

    def draw(self):
        # if hits == 0: don't draw or collide
        # different colour based on hit count
        pass

    def update(self):
        pass
