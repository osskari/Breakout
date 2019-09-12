from objects import *

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


# globals
screen_dimensions = (800, 600)
clock = None
level = None


# Initialise game
def init_game():
    global clock, level

    # Define clock
    clock = pygame.time.Clock()
    # Init pygame and set opengl as the renderer
    pygame.display.init()
    pygame.display.set_mode(screen_dimensions, DOUBLEBUF | OPENGL)
    glClearColor(0.0, 0.0, 0.0, 1.0)

    # Create all the game objects
    level = Level(Paddle(Point(400, 50), 500), Ball(Point(400, 300), 500))
    # Initial tick of the clock
    clock.tick()


# Updates game objects
def update():
    # Tick clock each time
    delta_time = clock.tick() / 1000.0

    # Updates game objects
    level.update(delta_time)


# Draws objects on the screen
def display():
    # Set up for drawing
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # set the viewport
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)

    # Draws objects
    level.draw()

    # Updates the display
    pygame.display.flip()


# Handles input from user
def events():
    # loops through all events
    for event in pygame.event.get():
        # quits game
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        # When a key is pressed
        elif event.type == pygame.KEYDOWN:
            # Escape
            if event.key == K_ESCAPE:
                pygame.quit()
                quit()
            # Left
            elif event.key == K_LEFT:
                level.player.direction[PADDLE_LEFT] = True
            # Right
            elif event.key == K_RIGHT:
                level.player.direction[PADDLE_RIGHT] = True
            # Space
            elif event.key == K_SPACE:
                level.ball.in_play = True
        # When a key is released
        elif event.type == pygame.KEYUP:
            # Left
            if event.key == K_LEFT:
                level.player.direction[0] = False
            # Right
            elif event.key == K_RIGHT:
                level.player.direction[1] = False


# Loop that runs each tick
def game_loop():
    events()
    update()
    display()


# The game
if __name__ == '__main__':
    init_game()
    while True:
        game_loop()
