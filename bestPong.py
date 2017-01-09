# PONG!!!!!

import pygame
import sys
import random
import math

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PONG_TABLE_COL = (44, 162, 95)

SCREEN_SIZE = (500, 500)  # window size is a 2-tuple measured in px

pygame.init()  # initialize the pygame system

screen = pygame.display.set_mode(SCREEN_SIZE)

# Initialize the clock
clock = pygame.time.Clock()


# Options
N_BALLS = 11
SPEED_FACT = .4
SPEED_ACC = 1.05

# Advanced options
PADDLE_LEN = 100
PADDLE_WIDTH = 10
BALL_WIDTH = 15
BALL_SPEED_FACTOR = 1
FPS = 240
DIRECT_CHANGE = 0.03
PADDLE_SPEED = 2


def initial_ball_speed():
    ball_speed = (random.choice([-3, 3]) * SPEED_FACT,
                  random.choice([-1, -0.5, -0.2, 0.2, 0.5, 1]) * SPEED_FACT)

    return ball_speed

def initial_screen():
    screen.fill(PONG_TABLE_COL)  # RGB white color tuple

    screen.fill(PONG_TABLE_COL)
    myfont1 = pygame.font.SysFont("monospace", 60)
    myfont2 = pygame.font.SysFont("monospace", 20)
    myfont3 = pygame.font.SysFont("monospace", 20)
    myfont4 = pygame.font.SysFont("monospace", 20)

    # render text
    label1 = myfont1.render("bestPONG", 1, WHITE)
    label2 = myfont2.render("W/S - left player", 1, WHITE)
    label3 = myfont3.render("UP/DOWN - right player", 1, WHITE)
    label4 = myfont4.render("press SPACE to start", 1, WHITE)

    screen.blit(label1, (200, 150))
    screen.blit(label2, (50, 300))
    screen.blit(label3, (50, 350))
    screen.blit(label4, (250, 450))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

        space_pressed = pygame.key.get_pressed()[pygame.K_SPACE]

        if space_pressed:
            break

def ending_screen(score):

    if score[0] >= N_BALLS:
        win_msg = "Left Won"
    elif score[1] >= N_BALLS:
        win_msg = "Right Won"

    screen.fill(PONG_TABLE_COL)
    myfont1 = pygame.font.SysFont("monospace", 60)
    myfont2 = pygame.font.SysFont("monospace", 40)
    myfont3 = pygame.font.SysFont("monospace", 25)

    # render text
    label1 = myfont1.render(win_msg, 1, WHITE)
    label2 = myfont2.render(str(score[0]) + ":" + str(score[1]), 1, WHITE)
    label3 = myfont3.render("press SPACE for new game", 1, WHITE)
    screen.blit(label1, (150, 200))
    screen.blit(label2, (200, 100))
    screen.blit(label3, (50, 450))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

        space_pressed = pygame.key.get_pressed()[pygame.K_SPACE]

        if space_pressed:
            break

    main()


def drawing(ball_pos, paddle1_pos, paddle2_pos, score):
    screen.fill(PONG_TABLE_COL)  # RGB white color tuple
    pygame.draw.circle(screen, WHITE, (round(ball_pos[0]), round(ball_pos[1])),
                       BALL_WIDTH)
    pygame.draw.line(screen, WHITE, (PADDLE_WIDTH, 0),
                     (PADDLE_WIDTH, SCREEN_SIZE[0]), 2)
    pygame.draw.line(screen, WHITE, (SCREEN_SIZE[1] - PADDLE_WIDTH, 0),
                     (SCREEN_SIZE[1] - PADDLE_WIDTH, SCREEN_SIZE[0]), 2)
    pygame.draw.rect(screen, WHITE,
                     (0, paddle1_pos[0], PADDLE_WIDTH, PADDLE_LEN))
    pygame.draw.rect(screen, WHITE,
                     (paddle2_pos[1], paddle2_pos[0],
                      PADDLE_WIDTH, PADDLE_LEN))

    myfont = pygame.font.SysFont("monospace", 40)

    # render text
    label = myfont.render(str(score[0]) + ":" + str(score[1]), 1, WHITE)
    screen.blit(label, (200, 100))

    pygame.display.update()

def ball_update(score, ball_pos, ball_speed, paddle1_pos, paddle2_pos):
    global time

    # Ball position
    if time > 150:
        ball_pos = (ball_pos[0] + ball_speed[0], ball_pos[1] + ball_speed[1])

    paddle1_top = paddle1_pos[0]
    paddle1_mid = paddle1_pos[0] + PADDLE_LEN / 2
    paddle1_bot = paddle1_pos[0] + PADDLE_LEN

    paddle2_top = paddle2_pos[0]
    paddle2_mid = paddle2_pos[0] + PADDLE_LEN / 2
    paddle2_bot = paddle2_pos[0] + PADDLE_LEN

    ball_left_edge_x = ball_pos[0] - BALL_WIDTH
    ball_right_edge_x = ball_pos[0] + BALL_WIDTH

    ball_hit_wall_left = ball_left_edge_x < 0 - PADDLE_WIDTH
    ball_hit_wall_right = ball_right_edge_x > SCREEN_SIZE[0] + PADDLE_WIDTH

    ball_hit_paddle_left = (paddle1_pos[1] + ball_speed[0]) <= ball_left_edge_x <= paddle1_pos[1] and \
                           (paddle1_top <= (ball_pos[1] + BALL_WIDTH) and paddle1_bot >= (ball_pos[1] - BALL_WIDTH))

    ball_hit_paddle_right = paddle2_pos[1] <= ball_right_edge_x <= (paddle2_pos[1] + ball_speed[0]) and \
                            (paddle2_top <= (ball_pos[1] + BALL_WIDTH) and paddle2_bot >= (ball_pos[1] - BALL_WIDTH))

    # Odraz od paddle
    if ball_hit_paddle_left or ball_hit_paddle_right:

        if ball_hit_paddle_left:
            ref_vec = (1, DIRECT_CHANGE * (ball_pos[1] - paddle1_mid) / PADDLE_WIDTH)
        else:
            ref_vec = (-1, DIRECT_CHANGE * (ball_pos[1] - paddle2_mid) / PADDLE_WIDTH)

        ref_vec_len = math.sqrt(ref_vec[0] ** 2 + ref_vec[1] ** 2)
        ref_vec_norm = (ref_vec[0] / ref_vec_len, ref_vec[1] / ref_vec_len)
        dot_prod = ref_vec_norm[0] * ball_speed[0] + ref_vec_norm[1] * ball_speed[1]

        ball_speed = ((ball_speed[0] - 2 * dot_prod * ref_vec_norm[0]) * SPEED_ACC,
                      (ball_speed[1] - 2 * dot_prod * ref_vec_norm[1]) * SPEED_ACC)

    # Odraz od steny
    if (ball_pos[1] - BALL_WIDTH) < 0 or (ball_pos[1] + BALL_WIDTH) > SCREEN_SIZE[1]:
        ball_speed = (ball_speed[0], -ball_speed[1])

    # Prohrana vymena
    if ball_hit_wall_left or ball_hit_wall_right:
        ball_pos = (250, 250)
        ball_speed = initial_ball_speed()

        if ball_hit_wall_left:
            score = (score[0], score[1] + 1)
        else:
            score = (score[0] + 1, score[1])

        time = 1

    else:
        time += 1

    return score, ball_pos, ball_speed, time

def main():

    global time

    # initial state
    ball_pos = (250, 250)
    ball_speed = initial_ball_speed()
    paddle1_pos = (250 - PADDLE_LEN / 2, PADDLE_WIDTH)
    paddle2_pos = (250 - PADDLE_LEN / 2, SCREEN_SIZE[1] - PADDLE_WIDTH)
    score = (0, 0)
    time = 0

    while True:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

        if time == 0:
            initial_screen()

#        time += 1

        key_press = pygame.key.get_pressed()

        # Paddle position
        if key_press[pygame.K_w] == 1 and (paddle1_pos[0]) >= 0:
            paddle1_pos = (paddle1_pos[0] - PADDLE_SPEED, paddle1_pos[1])
        elif key_press[pygame.K_s] == 1 and (paddle1_pos[0]) <= SCREEN_SIZE[1] - PADDLE_LEN:
            paddle1_pos = (paddle1_pos[0] + PADDLE_SPEED, paddle1_pos[1])

        if key_press[pygame.K_UP] == 1 and (paddle2_pos[0]) >= 0:
            paddle2_pos = (paddle2_pos[0] - PADDLE_SPEED, paddle2_pos[1])
        elif key_press[pygame.K_DOWN] == 1 and (paddle2_pos[0]) <= SCREEN_SIZE[1] - PADDLE_LEN:
            paddle2_pos = (paddle2_pos[0] + PADDLE_SPEED, paddle2_pos[1])

        [score, ball_pos, ball_speed, time] = ball_update(score, ball_pos, ball_speed, paddle1_pos, paddle2_pos)

        if score[0] >= N_BALLS or score[1] >= N_BALLS:
            ending_screen(score)
        else:
            drawing(ball_pos, paddle1_pos, paddle2_pos, score)

main()
