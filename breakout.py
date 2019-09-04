from .objects import *

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


# globals
clock = None


def init_game():
    global clock

    clock = pygame.time.Clock()
    pygame.display.init()
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    clock.tick()


def update():
    global clock

    delta_time = clock.tick() / 1000.0

    # update stuff


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glViewport(0, 0, 800, 600)
    gluOrtho2D(0, 800, 0, 600)

    # draw stuff

    pygame.display.flip()


def game_loop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    update()
    display()


if __name__ == '__main__':
    init_game()
    while True:
        game_loop()
