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
            self.position = paddle_position
        self.position += self.motion * delta_time

    def collision(self, delta_time, grid):
        window_points = [Point(0, 0), Point(WINDOW_WIDTH, 0), Point(WINDOW_WIDTH, 0),
                         Point(WINDOW_WIDTH, WINDOW_HEIGHT)]
        window_n = (Vector(-1, 0), Vector(1, 0), Vector(0, -1), Vector(0, 1))
        for p, n in zip(window_points, window_n):
            t_hit = thit(n, p, self.position, self.motion * delta_time)
            if 1 >= t_hit >= 0:
                self.motion = reflection(self.motion, n)
        block_bt = Vector(0, 1)
        block_lr = Vector(1, 0)
        for p in grid:
            t_hit_bt = thit(block_bt, p.position, self.position, self.motion * delta_time)
            t_hit_lr = thit(block_lr, p.position, self.position, self.motion * delta_time)
            if t_hit_bt < t_hit_lr:
                if 1 >= t_hit_bt >= 0:
                    p_hit = phit(self.position, t_hit_bt, self.motion)
                    if p_hit.is_between_x(p.position.x, p.position.x + BRICK_WIDTH):
                        self.motion = reflection(self.motion, block_bt)
                        # p.hit()
            else:
                if 1 >= t_hit_lr >= 0:
                    p_hit = phit(self.position, t_hit_bt, self.motion)
                    if p_hit.is_between_y(p.position.y, p.position.y + BRICK_HEIGHT):
                        self.motion = reflection(self.motion, block_lr)
                        # p.hit()


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
        x = ((BRICK_WIDTH * index.x) + GRID_REMAINDER_WIDTH // 2) + index.x
        y = ((WINDOW_HEIGHT - BRICK_HEIGHT) - BRICK_HEIGHT * index.y) - index.y
        return Point(x, y)

    def draw(self):
        # if hits == 0: don't draw or collide
        # different colour based on hit count
        glColor3f(self.colors[self.hits][RED], self.colors[self.hits][GREEN], self.colors[self.hits][BLUE])

        glPushMatrix()

        glTranslate(self.position.x, self.position.y, 0)

        glBegin(GL_TRIANGLES)
        glVertex2f(0, 0)
        glVertex2f(BRICK_WIDTH, 0)
        glVertex2f(0, BRICK_HEIGHT)

        glVertex2f(BRICK_WIDTH, 0)
        glVertex2f(0, BRICK_HEIGHT)
        glVertex2f(BRICK_WIDTH, BRICK_HEIGHT)
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
