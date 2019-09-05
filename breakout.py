from objects import *

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


# globals
screen_dimensions = (800, 600)
clock = None
player = None
ball = None


def init_game():
    global clock, player, ball

    clock = pygame.time.Clock()
    pygame.display.init()
    pygame.display.set_mode(screen_dimensions, DOUBLEBUF | OPENGL)
    glClearColor(0.0, 0.0, 0.0, 1.0)

    player = Paddle(Point(400, 50), 200)
    ball = Ball(Point(400, 300))

    clock.tick()


def update():
    global clock, player

    delta_time = clock.tick() / 1000.0

    # update stuff
    player.update(delta_time)


def display():
    global player, ball

    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glViewport(0, 0, 800, 600)
    gluOrtho2D(0, 800, 0, 600)

    # draw stuff
    player.draw((1.0, 0.0, 0.0))
    ball.draw((1.0, 0.0, 0.0))

    pygame.display.flip()


def game_loop():
    global player

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                quit()
            elif event.key == K_LEFT:
                player.direction[0] = True
            elif event.key == K_RIGHT:
                player.direction[1] = True
        elif event.type == pygame.KEYUP:
            if event.key == K_LEFT:
                player.direction[0] = False
            elif event.key == K_RIGHT:
                player.direction[1] = False

    update()
    display()


if __name__ == '__main__':
    init_game()
    while True:
        game_loop()
