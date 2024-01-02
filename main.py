import argparse
import random
import os
from datetime import datetime

import pygame as pg
import pygame.event
from matplotlib import pyplot as plt

from ball import Ball
from paddle import Paddle
import crisp_system
from fuzzy_system import FuzzySystem

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--paddle1', type=str, default='input', help='Paddle 1 movement system (input, crisp, fuzzy)')
    parser.add_argument('--paddle2', type=str, default='fuzzy', help='Paddle 2 movement system (input, crisp, fuzzy)')
    parser.add_argument('--view', type=bool, default=False, help='View fuzzy system (true, false)')
    parser.add_argument('--log', type=bool, default=False, help='Log game data (true, false)')
    parser.add_argument('--width', type=int, default=1024, help='Window width (px)')
    parser.add_argument('--height', type=int, default=768, help='Window height (px)')
    parser.add_argument('--speed', type=float, default=1000.0, help='Paddle speed (px/s)')
    parser.add_argument('--max_speed', type=float, default=800.0, help='Paddle max speed (px/s)')
    parser.add_argument('--ball_speed', type=float, default=800.0, help='Ball speed (px/s)')
    parser.add_argument('--max_angle_variation', type=float, default=45.0, help='Max angle variation (deg)')
    parser.add_argument('--paddle_size', type=int, default=100, help='Paddle size (px)')
    parser.add_argument('--score', type=int, default=-1, help='Score to win (points)')
    parser.add_argument('--games', type=int, default=1, help='Number of games to play')
    parser.add_argument('--nogui', type=bool, default=False, help='Disable GUI (true, false)')
    args = parser.parse_args()

    log_file = None

    if args.log:
        if not os.path.exists('logs'):
            os.makedirs('logs')
        log_file = open('logs/' + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.txt', 'w')

    def log(message: str):
        if args.log:
            log_file.write(message + '\n')
        if args.nogui:
            print(message)

    log('Paddle 1 system: ' + args.paddle1)
    log('Paddle 2 system: ' + args.paddle2)
    log('Paddle speed: ' + str(args.speed))
    log('Paddle max speed: ' + str(args.max_speed))
    log('Ball speed: ' + str(args.ball_speed))
    log('Max angle variation: ' + str(args.max_angle_variation))
    log('Paddle size: ' + str(args.paddle_size))
    log('Score to win: ' + str(args.score))

    games_won = [0, 0]

    for i in range(args.games):
        log('Game ' + str(i + 1) + ' started')

        score = [0, 0]
        paddle1 = Paddle(10, args.height // 2 - 50, args.paddle_size, args.speed, args.max_speed)
        paddle2 = Paddle(args.width - 20, args.height // 2 - 50, args.paddle_size, args.speed, args.max_speed)
        ball = Ball(args.width // 2, args.height // 2, 5, args.ball_speed/2)

        fuzzy_system = FuzzySystem(args.height, args.paddle_size, args.max_speed, args.ball_speed, args.view)

        paddle1_system = args.paddle1
        paddle2_system = args.paddle2

        if paddle1_system == 'crisp':
            paddle1_system = crisp_system
        if paddle2_system == 'crisp':
            paddle2_system = crisp_system
        if paddle1_system == 'fuzzy':
            paddle1_system = fuzzy_system
        if paddle2_system == 'fuzzy':
            paddle2_system = fuzzy_system

        font = None
        screen = None
        if not args.nogui:
            plt.show()
            pg.init()
            font = pg.font.Font("freesansbold.ttf", 32)
            screen = pg.display.set_mode((args.width, args.height))
            pg.display.set_caption("Fuzzy Pong")

        up_pressed = False
        down_pressed = False
        left_pressed = False
        right_pressed = False
        shift_pressed = False

        clock = pg.time.Clock()

        running = True
        while running:
            delta = clock.tick() / 1000

            speed = 0
            if not args.nogui:
                for event in pygame.event.get():
                    if event.type == pg.QUIT:
                        running = False
                        break
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_UP:
                            up_pressed = True
                        if event.key == pg.K_DOWN:
                            down_pressed = True
                        if event.key == pg.K_LEFT:
                            left_pressed = True
                        if event.key == pg.K_RIGHT:
                            right_pressed = True
                        if event.key == pg.K_LSHIFT:
                            shift_pressed = True
                    if event.type == pg.KEYUP:
                        if event.key == pg.K_UP:
                            up_pressed = False
                        if event.key == pg.K_DOWN:
                            down_pressed = False
                        if event.key == pg.K_LEFT:
                            left_pressed = False
                        if event.key == pg.K_RIGHT:
                            right_pressed = False
                        if event.key == pg.K_LSHIFT:
                            shift_pressed = False

                if up_pressed and not down_pressed:
                    speed = -1
                    if shift_pressed:
                        speed = -2
                if down_pressed and not up_pressed:
                    speed = 1
                    if shift_pressed:
                        speed = 2

            paddle_speed_outputs = []

            for (paddle_system, paddle) in [(paddle1_system, paddle1), (paddle2_system, paddle2)]:
                if paddle_system == 'input':
                    paddle.move(speed, delta)
                    paddle_speed_outputs.append(speed)
                else:
                    paddle_speed_outputs.append(paddle_system.move_paddle(paddle, ball, delta))

            if left_pressed and not right_pressed:
                ball.angle -= 1
            if right_pressed and not left_pressed:
                ball.angle += 1

            if not args.nogui:
                pg.draw.rect(screen, (0, 0, 0), (0, 0, args.width, args.height))
            for paddle in [paddle1, paddle2]:
                paddle.update(delta)
                if paddle.y <= 0.0:
                    paddle.y = 0.0
                    paddle.velocity = 0.0
                if paddle.y >= args.height - paddle.width:
                    paddle.y = args.height - paddle.width
                    paddle.velocity = 0.0

            ball.update(delta)

            if ball.y <= 0.0 or ball.y >= args.height:
                ball.angle = 360.0 - ball.angle
            if ball.x <= 0.0:
                score[1] += 1
                if args.log:
                    log('Paddle 2 scored: ' + str(score))
                ball.x = args.width / 2.0
                ball.y = args.height / 2.0
                ball.speed = args.ball_speed / 2
                ball.angle = random.randint(0, 360)
            if ball.x >= args.width:
                score[0] += 1
                if args.log:
                    log('Paddle 1 scored: ' + str(score))
                ball.x = args.width / 2.0
                ball.y = args.height / 2.0
                ball.speed = args.ball_speed / 2
                ball.angle = random.randint(0, 360)
            if paddle1.x <= ball.x <= paddle1.x + 10 and paddle1.y <= ball.y <= paddle1.y + paddle1.width:
                angle_variation = (ball.y - paddle1.y) / (paddle1.width / 2) - 1
                ball.angle = 180.0 - ball.angle + angle_variation * args.max_angle_variation
                ball.speed = args.ball_speed
            if paddle2.x >= ball.x >= paddle2.x - 10 and paddle2.y <= ball.y <= paddle2.y + paddle2.width:
                angle_variation = (ball.y - paddle2.y) / (paddle2.width / 2) - 1
                ball.angle = 180.0 - ball.angle - angle_variation * args.max_angle_variation
                ball.speed = args.ball_speed

            if args.score != -1 and (score[0] >= args.score or score[1] >= args.score):
                if args.log:
                    log('Game ended')
                    log(str(score))
                running = False
                if score[0] > score[1]:
                    games_won[0] += 1
                else:
                    games_won[1] += 1
                break

            ball_delta_y_input = ball.y - (paddle1.y + paddle1.width / 2)
            ball_delta_y_input_2 = ball.y - (paddle2.y + paddle2.width / 2)

            if not args.nogui:
                paddle1.draw(screen)
                paddle2.draw(screen)
                ball.draw(screen)
                score_text = font.render(str(score[0]) + " - " + str(score[1]), True, (255, 255, 255))
                score_text_rect = score_text.get_rect()
                score_text_rect.center = (args.width / 2, 32)
                output_text = font.render('Paddle 1 output: ' + '{:.2f}'.format(paddle_speed_outputs[0]), True, (255, 255, 255))
                output_text_rect = output_text.get_rect()
                output_text_rect.center = (args.width / 2, 64)
                output2_text = font.render('Paddle 2 output: ' + '{:.2f}'.format(paddle_speed_outputs[1]), True, (255, 255, 255))
                output2_text_rect = output2_text.get_rect()
                output2_text_rect.center = (args.width / 2, 96)
                ball_input_text = font.render('Paddle 1 ball delta: ' + '{:.2f}'.format(ball_delta_y_input), True, (255, 255, 255))
                ball_input_text_rect = ball_input_text.get_rect()
                ball_input_text_rect.center = (args.width / 2, 128)
                ball_input2_text = font.render('Paddle 2 ball delta: ' + '{:.2f}'.format(ball_delta_y_input_2), True, (255, 255, 255))
                ball_input2_text_rect = ball_input2_text.get_rect()
                ball_input2_text_rect.center = (args.width / 2, 160)
                paddle_input_text = font.render('Paddle 1 velocity: ' + '{:.2f}'.format(paddle1.velocity), True,
                                                (255, 255, 255))
                paddle_input_text_rect = paddle_input_text.get_rect()
                paddle_input_text_rect.center = (args.width / 2, 192)
                paddle2_input_text = font.render('Paddle 2 velocity: ' + '{:.2f}'.format(paddle2.velocity), True,
                                                (255, 255, 255))
                paddle2_input_text_rect = paddle2_input_text.get_rect()
                paddle2_input_text_rect.center = (args.width / 2, 224)
                screen.blit(score_text, score_text_rect)
                screen.blit(output_text, output_text_rect)
                screen.blit(output2_text, output2_text_rect)
                screen.blit(ball_input_text, ball_input_text_rect)
                screen.blit(ball_input2_text, ball_input2_text_rect)
                screen.blit(paddle_input_text, paddle_input_text_rect)
                screen.blit(paddle2_input_text, paddle2_input_text_rect)

                pg.display.flip()

    log('Games won: ' + str(games_won))

if __name__ == "__main__":
    main()
