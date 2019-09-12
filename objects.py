
import pygame
from OpenGL.GL import *

from v_math import *
from globals import *


# The paddle that bounces the ball from hitting the bottom plane
class Paddle:
    def __init__(self, position, speed):
        self.position = position        # x, and y coordinates of the paddle
        self.motion = Vector(0, 0)      # The motion of the paddle
        self.speed = speed              # The speed the paddle can move
        self.direction = [False, False] # Boolean on which direction the paddle is moving
        self.sides = self.set_sides()   # list of sides on the paddle that the ball might hit

    # Initiating the sides on the paddle that the ball might hit
    def set_sides(self):
        return [WindowBorder(self.position + Point(0, PADDLE_HEIGHT), Vector(0, 1), PADDLE_WIDTH, True),
                WindowBorder(self.position, Vector(1, 0), PADDLE_HEIGHT, False),
                WindowBorder(self.position + Point(PADDLE_WIDTH, 0), Vector(1, 0), PADDLE_HEIGHT, False)]

    # Draw the paddle
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

    # Updates the position of the paddle if the paddle is moving
    def update(self, delta_time):
        if self.direction[PADDLE_LEFT] and self.position.x > 0:
            self.motion = Vector(self.speed, 0)
            self.position -= self.motion * delta_time
        if self.direction[PADDLE_RIGHT] and self.position.x + PADDLE_WIDTH < WINDOW_WIDTH:
            self.motion = Vector(self.speed, 0)
            self.position += self.motion * delta_time
        self.sides = self.set_sides()


# Class that represents the projectile that hits the bricks
class Ball:
    def __init__(self, position, speed):
        self.position = position    # x, y cooridantes of the ball
        self.motion = Vector(0, 0)  # The motion of the ball
        self.speed = speed          # The speed of the paddle
        self.angle = 320            # The angle of the ball
        self.in_play = False        # True if the player has initiated the game
        self.radius = 5             # The radius of the ball
        self.hit = True             # True if the ball hits paddle

    def draw(self, b_color):
        glColor3f(b_color[RED], b_color[GREEN], b_color[BLUE])

        glPushMatrix()

        glTranslate(self.position.x, self.position.y, 0)

        glPointSize(4)

        glBegin(GL_POINTS)
        glVertex2f(0, 0)
        glEnd()

        glPopMatrix()

    # Updates the position of the ball
    def update(self, delta_time, paddle_position, grid, borders, paddle):
        # if not in play attach to top middle of paddle
        if self.in_play:
            if self.hit:
                self.motion = Vector(-m.sin(self.angle * m.pi / 180.0), m.cos(self.angle * m.pi / 180.0)) * self.speed
                self.hit = False
            self.motion = self.collision(delta_time, grid, borders, paddle, self.motion, self.position, None)
            self.motion = self.motion.normalize() * self.speed
                
        else:
            self.motion = Vector(0, 0)
            self.position = Point(paddle_position.x + PADDLE_WIDTH//2, paddle_position.y + PADDLE_HEIGHT//2)
        self.position += self.motion * delta_time
        # print(direction)

    # Recursive function that checks if the ball has collided with an object or the borders
    def collision(self, delta_time, grid, borders, paddle, motion, position, hit):
        smallest = None     # an object that holds the object with the smallest thit time
        tmpmotion = None    # Temporary variable holding the new motion for checking in the recursion
        # Detect collision with screen borders
        for border in borders:
            t_hit = thit(border.normal, border.position, position, motion)
            p_hit = phit(position, t_hit, motion)
            if hit is None or hit != border:
                if collision(border.position, position, motion, delta_time, border.direction, border.offset, smallest, t_hit):
                    smallest = (t_hit, border.normal, None, p_hit, border)
        # Detect collision with bricks
        for brick in grid:
            for side in brick.sides:
                t_hit = thit(side.normal, side.position, position, motion)
                p_hit = phit(position, t_hit, motion)
                if hit is None or hit != brick:
                    if collision(brick.position, position, motion, delta_time, side.direction, side.offset, smallest, t_hit):
                        # print(phit(position, t_hit, motion))
                        smallest = (t_hit, side.normal, brick, p_hit, brick)
        # detect collision with player controlled paddle
        for side in paddle.sides:
            t_hit = thit(side.normal, side.position, position, motion)
            p_hit = phit(position, t_hit, motion)
            if hit is None or hit != side:
                if collision(paddle.position, position, motion, delta_time, side.direction, side.offset, smallest, t_hit):
                    smallest = (t_hit, side.normal, paddle_angle(BASE_ANGLE, paddle.position + Point(PADDLE_WIDTH, PADDLE_HEIGHT), phit(position, t_hit, motion), ANGLE_DELTA, PADDLE_WIDTH), p_hit, side)

        if smallest is not None:
            tmpmotion = reflection(motion - (smallest[3] - position), smallest[1])
            if isinstance(smallest[2], Brick):  # Checks if the ball hit a brick
                smallest[2].hit()
            elif smallest[2] is not None:  # If the paddle is hit
                self.angle = smallest[2]
                self.hit = True
            else:                           # checks if the ball has hit the bottom
                if smallest[4].position == Point(0, 0) and smallest[4].normal == Vector(0, 1):
                    pygame.quit()
                    quit()

        if tmpmotion:
            # Runs if the ball collided with some object and calls recursively at collision function
            motion = tmpmotion
            motion = self.collision(delta_time, grid, borders, paddle, motion, smallest[3], smallest[4])
        return motion


# Class that represents the bricks that the player is suppose to clear the screen of
class Brick:
    def __init__(self, position, hits):
        self.position = self.set_pos(position)      # x, y coordinates of the brick
        self.hits = hits                            # hit points of the brick
        # the colors representing each hit on the brick
        self.colors = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]
        self.sides = self.set_sides()               # The sides of the brick

    # Overriding the equality sign
    def __eq__(self, other):
        if isinstance(other, Brick):
            return self.position.x == other.position.x and self.position.y == other.position.y
        else:
            return False

    # Called when ball hits a brick
    def hit(self):
        if self.hits > 0:
            self.hits -= 1

    # All sides of the brick that the ball could collide with
    def set_sides(self):
        return [WindowBorder(self.position, Vector(0, 1), BRICK_WIDTH, True),
                WindowBorder(self.position, Vector(1, 0), BRICK_HEIGHT, False),
                WindowBorder(self.position + Point(0, BRICK_HEIGHT), Vector(0, 1), BRICK_WIDTH, True),
                WindowBorder(self.position + Point(BRICK_WIDTH, 0), Vector(1, 0), BRICK_HEIGHT, False)]

    # Called when initiating the level
    @staticmethod
    def set_pos(index):
        x = ((BRICK_WIDTH * index.x) + GRID_REMAINDER_WIDTH//2)
        y = ((WINDOW_HEIGHT - BRICK_HEIGHT) - BRICK_HEIGHT * index.y) - 2 * BRICK_HEIGHT
        return Point(x, y)

    # Function to draw the brick on the window
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


# Class that governs each object of the game
class Level:
    def __init__(self, player, ball):
        self.player = player                # Paddle
        self.ball = ball                    # Ball
        self.grid = []                      # Grid holding the bricks
        self.borders = self.set_borders()   # Setting all the bricks to

        # initiates the grid with bricks
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                self.grid.append(Brick(Point(i, j), 3))

    # The border that the ball could hit
    @staticmethod
    def set_borders():
        return [WindowBorder(Point(0, 0), Vector(0, 1), WINDOW_WIDTH, True),
                WindowBorder(Point(0, 0), Vector(1, 0), WINDOW_HEIGHT, False),
                WindowBorder(Point(0, WINDOW_HEIGHT), Vector(0, 1), WINDOW_WIDTH, True),
                WindowBorder(Point(WINDOW_WIDTH, 0), Vector(1, 0), WINDOW_HEIGHT, False)]

    # Draws each object in the game
    def draw(self):
        self.player.draw((1.0, .0, 1.0))
        self.ball.draw((1.0, 1.0, 1.0))
        for i in self.grid:
            if i:
                i.draw()

    # Updates each object of the game
    def update(self, delta_time):
        self.ball.update(delta_time, Point(self.player.position.x, self.player.position.y + PADDLE_HEIGHT), self.grid,
                         self.borders, self.player)
        self.player.update(delta_time)
        self.grid = [i for i in self.grid if i.hits != 0]
        if len(self.grid) == 0:
            pygame.quit()
            quit()


# Class that defines the variables needed to calculate the collision and reflection
class WindowBorder:
    def __init__(self, position, normal, offset, direction):
        self.position = position    # x, y coordinates
        self.normal = normal        # The perpendicular normal vector of the line
        self.offset = offset        # The offset to the next point on the line
        self.direction = direction  # If its horizontal or vertical
