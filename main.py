import random
import pygame as pg
import pygame.event

from ball import Ball
from paddle import Paddle
from fuzzy_system import FuzzySystem


WIDTH = 800
HEIGHT = 600

SPEED = 1000.0
MAX_SPEED = 800.0

PADDLE_SIZE = 100

score = [0, 0]
paddle1 = Paddle(10, HEIGHT // 2 - 50, PADDLE_SIZE, SPEED, MAX_SPEED)
paddle2 = Paddle(WIDTH - 20, HEIGHT // 2 - 50, PADDLE_SIZE, SPEED, MAX_SPEED)
ball = Ball(WIDTH // 2, HEIGHT // 2, 5, 200.0)


def main():
    pg.init()
    font = pg.font.Font("freesansbold.ttf", 32)
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Fuzzy Pong")

    fuzzy_system = FuzzySystem(HEIGHT, PADDLE_SIZE, MAX_SPEED)

    up_pressed = False
    down_pressed = False
    left_pressed = False
    right_pressed = False
    shift_pressed = False

    clock = pg.time.Clock()

    running = True
    while running:
        delta = clock.tick() / 1000

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
            paddle1.move(speed, delta)
        if down_pressed and not up_pressed:
            speed = 1
            if shift_pressed:
                speed = 2
            paddle1.move(speed, delta)

        if left_pressed and not right_pressed:
            ball.angle -= 1
        if right_pressed and not left_pressed:
            ball.angle += 1

        ball_delta_y_input = ball.y - (paddle2.y + PADDLE_SIZE/2)
        paddle_velocity_input = paddle2.velocity

        paddle_speed_output = fuzzy_system.get_output(ball_delta_y_input, paddle_velocity_input)
        paddle2.move(paddle_speed_output, delta)

        pg.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
        for paddle in [paddle1, paddle2]:
            paddle.update(delta)
            if paddle.y <= 0.0:
                paddle.y = 0.0
                paddle.velocity = 0.0
            if paddle.y >= HEIGHT - paddle.width:
                paddle.y = HEIGHT - paddle.width
                paddle.velocity = 0.0

        ball.update(delta)

        if ball.y <= 0.0 or ball.y >= HEIGHT:
            ball.angle = 360.0 - ball.angle
        if ball.x <= 0.0:
            score[1] += 1
            ball.x = WIDTH / 2.0
            ball.y = HEIGHT / 2.0
            ball.angle = random.randint(0, 360)
        if ball.x >= WIDTH:
            score[0] += 1
            ball.x = WIDTH / 2.0
            ball.y = HEIGHT / 2.0
            ball.angle = random.randint(0, 360)
        if paddle1.x <= ball.x <= paddle1.x + 10 and paddle1.y <= ball.y <= paddle1.y + paddle1.width:
            ball.angle = 180.0 - ball.angle
        if paddle2.x >= ball.x >= paddle2.x - 10 and paddle2.y <= ball.y <= paddle2.y + paddle2.width:
            ball.angle = 180.0 - ball.angle

        paddle1.draw(screen)
        paddle2.draw(screen)
        ball.draw(screen)
        score_text = font.render(str(score[0]) + " - " + str(score[1]), True, (255, 255, 255))
        score_text_rect = score_text.get_rect()
        score_text_rect.center = (WIDTH / 2, 32)
        output_text = font.render('Paddle output: ' + '{:.2f}'.format(paddle_speed_output), True, (255, 255, 255))
        output_text_rect = output_text.get_rect()
        output_text_rect.center = (WIDTH / 2, 64)
        ball_input_text = font.render('Ball delta input: ' + '{:.2f}'.format(ball_delta_y_input), True, (255, 255, 255))
        ball_input_text_rect = ball_input_text.get_rect()
        ball_input_text_rect.center = (WIDTH / 2, 96)
        paddle_input_text = font.render('Paddle velocity input: ' + '{:.2f}'.format(paddle_velocity_input), True,
                                        (255, 255, 255))
        paddle_input_text_rect = paddle_input_text.get_rect()
        paddle_input_text_rect.center = (WIDTH / 2, 128)
        screen.blit(score_text, score_text_rect)
        screen.blit(output_text, output_text_rect)
        screen.blit(ball_input_text, ball_input_text_rect)
        screen.blit(paddle_input_text, paddle_input_text_rect)
        pg.display.flip()


if __name__ == "__main__":
    main()
