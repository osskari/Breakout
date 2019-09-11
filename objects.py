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

    def update(self, delta_time, paddle_position, grid, borders):
        # if not in play attach to top middle of paddle
        if self.in_play:
            if self.motion == Vector(0, 0):
                self.motion = Vector(-m.sin(self.angle * m.pi / 180.0), m.cos(self.angle * m.pi / 180.0)) * self.speed
            self.collision(delta_time, grid, borders)
        else:
            self.motion = Vector(0, 0)
            self.position = Point(paddle_position.x + PADDLE_WIDTH//2, paddle_position.y + PADDLE_HEIGHT//2)
        self.position += self.motion * delta_time

    def collision(self, delta_time, grid, borders):
        smallest = None

        for border in borders:
            t_hit = thit(border.normal, border.position, self.position, self.motion)
            if collision(border.position, self.position, self.motion, delta_time, border.direction, border.offset, smallest, t_hit):
                smallest = (t_hit, border.normal, None)

        for brick in grid:
            for side in brick.sides:
                t_hit = thit(side.normal, side.position, self.position, self.motion)
                if collision(brick.position, self.position, self.motion, delta_time, side.direction, side.offset, smallest, t_hit):
                    print(phit(self.position, t_hit, self.motion))
                    smallest = (t_hit, side.normal, brick)

        if smallest is not None:
            self.motion = reflection(self.motion, smallest[1])
            if isinstance(smallest[2], Brick):
                smallest[2].hit()


class Brick:
    def __init__(self, position, hits):
        self.position = self.set_pos(position)
        self.hits = hits
        self.colors = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]
        self.sides = self.set_sides()

    def hit(self):
        if self.hits > 0:
            self.hits -= 1

    def set_sides(self):
        return [WindowBorder(self.position, Vector(0, 1), BRICK_WIDTH, True),
                WindowBorder(self.position, Vector(1, 0), BRICK_HEIGHT, False),
                WindowBorder(self.position + Point(0, BRICK_HEIGHT), Vector(0, 1), BRICK_WIDTH, True),
                WindowBorder(self.position + Point(BRICK_WIDTH, 0), Vector(1, 0), BRICK_HEIGHT, False)]

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
        glVertex2f(0.5, 0.5)
        glVertex2f(BRICK_WIDTH - 0.5, 0.5)
        glVertex2f(0.5, BRICK_HEIGHT - 0.5)

        glVertex2f(BRICK_WIDTH - 0.5, 0.5)
        glVertex2f(0.5, BRICK_HEIGHT - 0.5)
        glVertex2f(BRICK_WIDTH - 0.5, BRICK_HEIGHT - 0.5)
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
        self.borders = self.set_borders()

        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                self.grid.append(Brick(Point(i, j), 2))

    @staticmethod
    def set_borders():
        return [WindowBorder(Point(0, 0), Vector(0, 1), WINDOW_WIDTH, True),
                WindowBorder(Point(0, 0), Vector(1, 0), WINDOW_HEIGHT, False),
                WindowBorder(Point(0, WINDOW_HEIGHT), Vector(0, 1), WINDOW_WIDTH, True),
                WindowBorder(Point(WINDOW_WIDTH, 0), Vector(1, 0), WINDOW_HEIGHT, False)]

    def draw(self):
        self.player.draw((1.0, 0.0, 0.0))
        self.ball.draw((1.0, 0.0, 0.0))
        for i in self.grid:
            if i:
                i.draw()

    def update(self, delta_time):
        self.player.update(delta_time)
        self.ball.update(delta_time, Point(self.player.position.x, self.player.position.y + PADDLE_HEIGHT), self.grid, self.borders)
        self.grid = [i for i in self.grid if i.hits != 0]


class WindowBorder:
    def __init__(self, position, normal, offset, direction):
        self.position = position
        self.normal = normal
        self.offset = offset
        self.direction = direction
