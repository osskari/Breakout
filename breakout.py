from objects import *

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


# globals
screen_dimensions = (800, 600)
clock = None
level = None


def init_game():
    global clock, level

    clock = pygame.time.Clock()
    pygame.display.init()
    pygame.display.set_mode(screen_dimensions, DOUBLEBUF | OPENGL)
    glClearColor(0.0, 0.0, 0.0, 1.0)

    level = Level(Paddle(Point(400, 50), 500), Ball(Point(400, 300), 400))

    clock.tick()


def update():
    delta_time = clock.tick() / 1000.0

    level.update(delta_time)


def display():

    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)

    level.draw()

    pygame.display.flip()


def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                quit()
            elif event.key == K_LEFT:
                level.player.direction[PADDLE_LEFT] = True
            elif event.key == K_RIGHT:
                level.player.direction[PADDLE_RIGHT] = True
            elif event.key == K_SPACE:
                level.ball.in_play = True
        elif event.type == pygame.KEYUP:
            if event.key == K_LEFT:
                level.player.direction[0] = False
            elif event.key == K_RIGHT:
                level.player.direction[1] = False


def game_loop():
    events()
    update()
    display()


if __name__ == '__main__':
    init_game()
    while True:
        game_loop()
