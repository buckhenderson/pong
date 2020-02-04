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
RED = (255, 0, 0)

# initialize some display parameters
size = [1000, 600]
paddle_height = 100
paddle_width = 20
top_area_y_pos = 30
top_area_height = 10
done = False
display_splash = True
regular_game_play = False
one_player_play = False
speed_increment = 1

def print_scores():
    font = pygame.font.Font('freesansbold.ttf', 28)
    text1 = font.render(str(player_1_points), True, WHITE, BLACK)
    text2 = font.render(str(player_2_points), True, WHITE, BLACK)
    text1_rect = text1.get_rect()
    text2_rect = text2.get_rect()
    text1_rect.center = 100, top_area_y_pos / 2
    text2_rect.center = size[0] - 100, top_area_y_pos / 2
    screen.blit(text1, text1_rect)
    screen.blit(text2, text2_rect)
    pygame.display.flip()
    return


class Paddle:
    def __init__(self, x_pos=100
                 , y_pos=((size[1] - (top_area_y_pos + top_area_height)) / 2) - paddle_height / 2 + (top_area_y_pos + top_area_height)
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
        if self.y_pos <= top_area_y_pos + top_area_height:
            self.y_pos = top_area_y_pos + top_area_height
        if self.y_pos >= size[1] - self.height:
            self.y_pos = size[1] - self.height


class Ball:
    def __init__(self, x_pos=200, y_pos=200, width=10, height=10, color=WHITE, overall_speed=5, angle=(1/4)*math.pi):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.color = color
        self.overall_speed = overall_speed
        self.speed = [self.overall_speed * math.cos(angle), self.overall_speed * math.sin(angle)]
        self.angle = angle
        self.spin = 0

    def reset(self):
        self.x_pos = 200
        self.y_pos = 200
        self.angle = (1/4)*math.pi

    def draw(self):
        pygame.draw.rect(screen, self.color, [self.x_pos, self.y_pos, self.width, self.height])

    def move(self):
        self.speed[0] = self.overall_speed*math.cos(self.angle)
        self.speed[1] = self.overall_speed*math.sin(self.angle)
        self.x_pos = self.x_pos + self.speed[0]
        self.y_pos = self.y_pos + self.speed[1]
        if self.x_pos <= 0:
            self.x_pos = 0
        if self.x_pos >= size[0] - self.width:
            self.x_pos = size[0] - self.width
        if self.x_pos >= size[0] - self.width or self.x_pos <= 0:
            self.speed[0] = self.speed[0] * -1
        if self.y_pos <= top_area_y_pos + top_area_height:
            self.y_pos = top_area_y_pos + top_area_height
        if self.y_pos >= size[1] - self.width:
            self.y_pos = size[1] - self.width
        if self.y_pos >= size[1] - self.width or self.y_pos <= top_area_y_pos + top_area_height:
            # self.speed[1] = self.speed[1] * -1
            self.angle = self.angle * -1


def check_paddle_1(paddle, ball):
    if paddle.x_pos <= ball.x_pos <= paddle.x_pos + paddle.width and \
            paddle.y_pos - paddle.width <= ball.y_pos < paddle.y_pos + paddle.height:
        # dateTimeObj = datetime.now()
        # timestampStr = dateTimeObj.strftime("%m_%d_%Y_%H_%M_%S_%f")
        # print('{}, x: {}, y: {}'.format(timestampStr, ball.x_pos, ball.y_pos))
        # pygame.image.save(screen, "C:/breakout/screenshot" + timestampStr + ".jpg")
        if ball.y_pos < paddle.y_pos + (1/5)*paddle.height:
            return_angle = (11/6)*math.pi
        elif paddle.y_pos + (1/5)*paddle.height <= ball.y_pos < paddle.y_pos + (2/5)*paddle.height:
            return_angle = (23/12)*math.pi
        elif paddle.y_pos + (2/5)*paddle.height <= ball.y_pos < paddle.y_pos + (3/5)*paddle.height:
            return_angle = 0
        elif paddle.y_pos + (3/5)*paddle.height <= ball.y_pos < paddle.y_pos + (4/5)*paddle.height:
            return_angle = (1/12)*math.pi
        else:
            return_angle = (1/6)*math.pi
        return return_angle
    else:
        return None

def check_paddle_2(paddle, ball):
    if paddle.x_pos <= ball.x_pos + ball.width <= paddle.x_pos + paddle_width and \
            paddle.y_pos - paddle.width <= ball.y_pos < paddle.y_pos + paddle.height:
        # dateTimeObj = datetime.now()
        # timestampStr = dateTimeObj.strftime("%m_%d_%Y_%H_%M_%S_%f")
        # print('{}, x: {}, y: {}'.format(timestampStr, ball.x_pos, ball.y_pos))
        # pygame.image.save(screen, "C:/breakout/screenshot" + timestampStr + ".jpg")
        if ball.y_pos < paddle.y_pos + (1 / 5) * paddle.height:
            return_angle = (7 / 6) * math.pi
        elif paddle.y_pos + (1 / 5) * paddle.height <= ball.y_pos < paddle.y_pos + (2 / 5) * paddle.height:
            return_angle = (13 / 12) * math.pi
        elif paddle.y_pos + (2 / 5) * paddle.height <= ball.y_pos < paddle.y_pos + (3 / 5) * paddle.height:
            return_angle = math.pi
        elif paddle.y_pos + (3 / 5) * paddle.height <= ball.y_pos < paddle.y_pos + (4 / 5) * paddle.height:
            return_angle = (11 / 12) * math.pi
        else:
            return_angle = (5 / 6) * math.pi
        return return_angle
    else:
        return None

def show_splash():
    font = pygame.font.Font('freesansbold.ttf', 32)
    text1 = font.render('!!!PONG!!!', True, WHITE, BLACK)
    text2 = font.render('A FOR 1-PLAYER', True, WHITE, BLACK)
    text3 = font.render('X FOR 2-PLAYER', True, WHITE, BLACK)
    text1_rect = text1.get_rect()
    text2_rect = text2.get_rect()
    text3_rect = text3.get_rect()
    screen.fill(BLACK)
    text1_rect.center = size[0]/2, size[1]/2 - 100
    text2_rect.center = size[0]/2, size[1]/2
    text3_rect.center = size[0]/2, size[1]/2 + 100
    screen.blit(text1, text1_rect)
    screen.blit(text2, text2_rect)
    screen.blit(text3, text3_rect)
    pygame.display.flip()
    return


def predict_player_2():
    x1, y1 = ball_state_list[0]
    x2, y2 = ball_state_list[1]
    if x2 - x1 < 0:
        return
    elif x2 == x1:
        return
    else:
        m = (y2 - y1) / (x2 - x1)
        m = math.sin(ball.angle)
        b = y1 - m*x1
        out_y = m*player_2.x_pos + b - (player_2.height / 2)
        pygame.draw.line(screen, WHITE, (ball.x_pos, ball.y_pos), (player_2.x_pos, out_y + player_2.height / 2))
        return out_y


# start the pygame app
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
screen = pygame.display.set_mode(size)
paddle_bounce = pygame.mixer.Sound('C:/Users/ben/PycharmProjects/pong/170142__timgormly__8-bit-blip1.wav')
score_sound = pygame.mixer.Sound('C:/Users/ben/PycharmProjects/pong/445978__breviceps__error-signal-2.wav')

pygame.display.set_caption("My Game")
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# initialize game components
player_1 = Paddle()
player_2 = Paddle(x_pos=size[0] - 100)
ball = Ball()
player_1_points = 0
player_2_points = 0
player_1_win_round = False
player_2_win_round = False
ball_state_list = []
i = 0
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif regular_game_play and event.type == pygame.KEYDOWN:
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
        elif regular_game_play and event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
            if event.key == pygame.K_q or event.key == pygame.K_a:
                player_1.speed = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_2.speed = 0
        elif display_splash and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                display_splash = False
                regular_game_play = True
                one_player_play = False
            if event.key == pygame.K_a:
                display_splash = False
                regular_game_play = True
                one_player_play = True
                player_2.color = RED


    # --- Game logic should go here
    if regular_game_play:
        ball.move()
        player_1.move()
        player_2.move()
        if ball.x_pos < player_1.x_pos + 100:
            paddle_result = check_paddle_1(player_1, ball)
            if paddle_result or paddle_result == 0:
                paddle_bounce.play()
                ball.angle = paddle_result
                speed_increment += 1
                paddle_result = None
        if ball.x_pos > player_2.x_pos - 100:
            paddle_result = check_paddle_2(player_2, ball)
            if paddle_result:
                paddle_bounce.play()
                ball.angle = paddle_result
                speed_increment += 1
                speed_increment = min(speed_increment, 9)
                paddle_result = None
        if ball.x_pos == 0:
            player_2_points += 1
            player_2_win_round = True
        if ball.x_pos == size[0] - ball.width:
            player_1_points += 1
            player_1_win_round = True
        if player_1_win_round or player_2_win_round:
            time.sleep(1)
            player_1_win_round = False
            player_2_win_round = False
            ball = Ball()
            speed_increment = 1
            score_sound.play()
        if speed_increment % 4 == 0:
            ball.overall_speed +=1
            speed_increment = 1
        screen.fill(BLACK)
        # --- Drawing code should go here
        pygame.draw.rect(screen, WHITE, [0, top_area_y_pos, size[0], top_area_height])
        for j in range(0, int(size[1] / 20)):
            if j % 2 == 0:
                color = BLACK
            else: color = WHITE
            if top_area_y_pos < j*20:
                pygame.draw.line(screen, color, (size[0] / 2, j*20), (size[0] / 2, (j + 1)* 20 ), 2)
        player_1.draw()
        player_2.draw()
        ball.draw()
        print_scores()

    if display_splash:
        show_splash()

    if one_player_play:
        i += 1
        if i % 30:
            ball_state_list.append([ball.x_pos, ball.y_pos])
            if len(ball_state_list) > 2:
                ball_state_list.pop(0)
            if len(ball_state_list) == 2:
                out_y = predict_player_2()
                # time.sleep(.1)
                if out_y:
                    multiplier = 1 if out_y > player_2.y_pos else -1
                    player_2.speed = multiplier * 5
                    player_2.move()
                    if abs((player_2.y_pos + (player_2.height / 2)) - out_y) < 10:
                        player_2.speed = 0
                else:
                    player_2.speed = 0



    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)
pygame.quit()