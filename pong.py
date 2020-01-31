import pygame
import math
import time
from datetime import datetime

# to debug, we'll print to log
########## having issues with this, works on one machine but not another
# import sys
# sys.stdout = open('C:/breakout/output.txt', 'w')
# print('test')


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

size = [800, 600]
paddle_height = 100
paddle_width = 20


class Paddle:
    def __init__(self, x_pos=100
                 , y_pos=(size[1] / 2) - paddle_height / 2
                 , width=paddle_width
                 , height=paddle_height
                 , color=WHITE):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.color = color
        self.speed = 0

    def draw(self):
        pygame.draw.rect(screen, self.color, [self.x_pos, self.y_pos, self.width, self.height])

    def move(self):
        self.y_pos = self.y_pos + self.speed
        if self.y_pos <= 0:
            self.y_pos = 0
        if self.y_pos >= size[1] - self.height:
            self.y_pos = size[1] - self.height


class Ball:
    def __init__(self, x_pos=200, y_pos=200, width=10, height=10, color=WHITE, speed=5, angle=.75*math.pi):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.color = color
        self.speed = [speed*math.cos(angle), speed*math.sin(angle)]
        self.angle = angle
        self.spin = 0

    def reset(self):
        self.x_pos = 200
        self.y_pos = 200
        self.angle = .75*math.pi

    def draw(self):
        pygame.draw.rect(screen, self.color, [self.x_pos, self.y_pos, self.width, self.height])

    def move(self):
        self.x_pos = self.x_pos + self.speed[0]*math.cos(self.angle)
        self.y_pos = self.y_pos + self.speed[1]*math.sin(self.angle)
        if self.x_pos <= 0:
            self.x_pos = 0
        if self.x_pos >= size[0] - self.width:
            self.x_pos = size[0] - self.width
        if self.x_pos >= size[0] - self.width or self.x_pos <= 0:
            self.speed[0] = self.speed[0] * -1
        if self.y_pos <= 0:
            self.y_pos = 0
        if self.y_pos >= size[1] - self.width:
            self.y_pos = size[1] - self.width
        if self.y_pos >= size[1] - self.width or self.y_pos <= 0:
            self.speed[1] = self.speed[1] * -1


done = False

# start the pygame app
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# initialize game components
player_1 = Paddle()
print(player_1.x_pos)
print(player_1.y_pos)
player_2 = Paddle(x_pos=size[0] - 100)
ball = Ball()

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            # player 1
            if event.key == pygame.K_q:
                player_1.speed = -6
            elif event.key == pygame.K_a:
                player_1.speed = 6
            # player 2
            if event.key == pygame.K_UP:
                player_2.speed = -6
            elif event.key == pygame.K_DOWN:
                player_2.speed = 6
            # User let up on a key
        elif event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
            if event.key == pygame.K_q or event.key == pygame.K_a:
                player_1.speed = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_2.speed = 0
    # --- Game logic should go here
    ball.move()
    player_1.move()
    player_2.move()


    screen.fill(BLACK)
    # --- Drawing code should go here
    player_1.draw()
    player_2.draw()
    ball.draw()

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

pygame.quit()