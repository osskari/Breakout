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
        self.motion = Vector(0, 0)
        self.speed = speed
        self.direction = [False, False]

    def draw(self, p_color):
        glColor3f(p_color[RED], p_color[GREEN], p_color[BLUE])

        glPushMatrix()

        glTranslate(self.position.x, self.position.y, 0)

        glBegin(GL_TRIANGLES)
        glVertex2f(0, 0)
        glVertex2f(PADDLE_WIDTH, 0)
        glVertex2f(0, PADDLE_HEIGHT)

        glVertex2f(PADDLE_WIDTH, 0)
        glVertex2f(0, PADDLE_HEIGHT)
        glVertex2f(PADDLE_WIDTH, PADDLE_HEIGHT)
        glEnd()

        glPopMatrix()

    def update(self, delta_time):
        if self.direction[PADDLE_LEFT] and self.position.x > 0:
            self.motion = Vector(self.speed, 0)
            self.position -= self.motion * delta_time
        if self.direction[PADDLE_RIGHT] and self.position.x + PADDLE_WIDTH < WINDOW_WIDTH:
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
        glColor3f(b_color[RED], b_color[GREEN], b_color[BLUE])

        glPushMatrix()

        glTranslate(self.position.x, self.position.y, 0)

        glPointSize(4)

        glBegin(GL_POINTS)
        glVertex2f(0, 0)
        glEnd()

        glPopMatrix()

    def update(self, delta_time, paddle_position, grid):
        # if not in play attach to top middle of paddle
        if self.in_play:
            if self.motion == Vector(0, 0):
                self.motion = Vector(-m.sin(self.angle * m.pi / 180.0), m.cos(self.angle * m.pi / 180.0)) * self.speed
            self.collision(delta_time, grid)
        else:
            self.motion = Vector(0, 0)
            self.position = Point(paddle_position.x + PADDLE_WIDTH//2, paddle_position.y + PADDLE_HEIGHT//2)
        self.position += self.motion * delta_time

    def collision(self, delta_time, grid):
        smallest = None
        normal_vert = Vector(0, 1)
        normal_horiz = Vector(1, 0)

        smallest = collision(normal_vert, Point(0, 0), self.position, self.motion, delta_time, True, WINDOW_WIDTH, smallest)
        smallest = collision(normal_vert, Point(0, WINDOW_HEIGHT), self.position, self.motion, delta_time, True, WINDOW_WIDTH, smallest)
        smallest = collision(normal_horiz, Point(0, 0), self.position, self.motion, delta_time, False, WINDOW_HEIGHT, smallest)
        smallest = collision(normal_horiz, Point(WINDOW_WIDTH, 0), self.position, self.motion, delta_time, False, WINDOW_HEIGHT, smallest)

        for p in grid:
            # bottom
            smallest = brick_collision(smallest, normal_vert, p, self, delta_time, 0, 0, True, BRICK_WIDTH, BRICK_HEIGHT)
            # top
            smallest = brick_collision(smallest, normal_vert, p, self, delta_time, 0, BRICK_HEIGHT, True, BRICK_WIDTH, BRICK_HEIGHT)
            # left
            smallest = brick_collision(smallest, normal_horiz, p, self, delta_time, 0, 0, False, BRICK_WIDTH, BRICK_HEIGHT)
            # right
            smallest = brick_collision(smallest, normal_horiz, p, self, delta_time, BRICK_WIDTH, 0, False, BRICK_WIDTH, BRICK_HEIGHT)

        if smallest is not None:
            self.motion = reflection(self.motion, smallest[1])
            if isinstance(smallest[2], Brick):
                smallest[2].hit()


class Brick:
    def __init__(self, position, hits):
        self.position = self.set_pos(position)
        self.hits = hits
        self.colors = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]

    def hit(self):
        if self.hits > 0:
            self.hits -= 1

    @staticmethod
    def set_pos(index):
        x = ((BRICK_WIDTH * index.x) + GRID_REMAINDER_WIDTH)
        y = ((WINDOW_HEIGHT - BRICK_HEIGHT) - BRICK_HEIGHT * index.y)
        return Point(x, y)

    def draw(self):
        # if hits == 0: don't draw or collide
        # different colour based on hit count
        glPushMatrix()

        glTranslate(self.position.x, self.position.y, 0)

        glBegin(GL_TRIANGLES)

        glColor3f(0.0, 0.0, 0.0)
        glVertex2f(0, 0)
        glVertex2f(BRICK_WIDTH, 0)
        glVertex2f(0, BRICK_HEIGHT)

        glVertex2f(BRICK_WIDTH, 0)
        glVertex2f(0, BRICK_HEIGHT)
        glVertex2f(BRICK_WIDTH, BRICK_HEIGHT)

        glColor3f(self.colors[self.hits][RED], self.colors[self.hits][GREEN], self.colors[self.hits][BLUE])
        glVertex2f(1, 1)
        glVertex2f(BRICK_WIDTH - 1, 1)
        glVertex2f(1, BRICK_HEIGHT - 1)

        glVertex2f(BRICK_WIDTH - 1, 1)
        glVertex2f(1, BRICK_HEIGHT - 1)
        glVertex2f(BRICK_WIDTH - 1, BRICK_HEIGHT - 1)
        glEnd()

        glPopMatrix()

    def update(self):
        pass


class Level:
    def __init__(self, player, ball, brick_count):
        self.player = player
        self.ball = ball
        self.brick_count = brick_count
        self.grid = []

        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                self.grid.append(Brick(Point(i, j), 2))

    def draw(self):
        self.player.draw((1.0, 0.0, 0.0))
        self.ball.draw((1.0, 0.0, 0.0))
        for i in self.grid:
            if i:
                i.draw()

    def update(self, delta_time):
        self.player.update(delta_time)
        self.ball.update(delta_time, Point(self.player.position.x, self.player.position.y + PADDLE_HEIGHT), self.grid)
        self.grid = [i for i in self.grid if i.hits != 0]
