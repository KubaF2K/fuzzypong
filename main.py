import math
import random
import pygame as pg
import pygame.event
# import skfuzzy as fuzz
# from skfuzzy import control as ctrl

WIDTH = 800
HEIGHT = 600


class Paddle:
    def __init__(self, x: int, y: int, width: int, speed: float, max_speed: float):
        self.x = x
        self.y = y
        self.width = width
        self.speed = speed
        self.velocity = 0.0
        self.max_speed = max_speed

    def move(self, direction: int, delta_time: float):
        self.velocity += direction * self.speed * delta_time
        self.velocity = max(min(self.velocity, self.max_speed), -self.max_speed)

    def update(self, delta_time: float):
        self.y += self.velocity * delta_time
        if self.y <= 0.0:
            self.y = 0.0
            self.velocity = 0.0
        if self.y >= HEIGHT - self.width:
            self.y = HEIGHT - self.width
            self.velocity = 0.0

    def draw(self, screen: pg.Surface):
        pg.draw.rect(screen, (255, 255, 255), (self.x, self.y, 10, self.width))

class Ball:
    def __init__(self, x: int, y: int, radius: int, speed: float):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.angle = random.randint(0, 360)

    def update(self, delta_time: float):
        self.x += self.speed * delta_time * math.cos(math.radians(self.angle))
        self.y += self.speed * delta_time * math.sin(math.radians(self.angle))
        if self.y <= 0.0 or self.y >= HEIGHT:
            self.angle = 360.0 - self.angle
        if self.x <= 0.0:
            score[1] += 1
            self.x = WIDTH / 2.0
            self.y = HEIGHT / 2.0
            self.angle = random.randint(0, 360)
        if self.x >= WIDTH:
            score[0] += 1
            self.x = WIDTH / 2.0
            self.y = HEIGHT / 2.0
            self.angle = random.randint(0, 360)
        if paddle1.x <= self.x <= paddle1.x + 10 and paddle1.y <= self.y <= paddle1.y + paddle1.width:
            self.angle = 180.0 - self.angle
        if paddle2.x >= self.x >= paddle2.x - 10 and paddle2.y <= self.y <= paddle2.y + paddle2.width:
            self.angle = 180.0 - self.angle

    def draw(self, screen: pg.Surface):
        pg.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius)


score = [0, 0]
paddle1 = Paddle(10, HEIGHT // 2 - 50, 100, 1000.0, 800.0)
paddle2 = Paddle(WIDTH - 20, HEIGHT // 2 - 50, 100, 1000.0, 800.0)
ball = Ball(WIDTH // 2, HEIGHT // 2, 5, 200.0)


def main():
    pg.init()
    font = pg.font.Font("freesansbold.ttf", 32)
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Fuzzy Pong")
    clock = pg.time.Clock()

    up_pressed = False
    down_pressed = False
    shift_pressed = False

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
                if event.key == pg.K_LSHIFT:
                    shift_pressed = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    up_pressed = False
                if event.key == pg.K_DOWN:
                    down_pressed = False
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

        #     TODO: Implement fuzzy logic

        pg.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
        paddle1.update(delta)
        paddle2.update(delta)
        ball.update(delta)
        paddle1.draw(screen)
        paddle2.draw(screen)
        ball.draw(screen)
        text = font.render(str(score[0]) + " - " + str(score[1]), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (WIDTH / 2, 32)
        screen.blit(text, text_rect)
        pg.display.flip()


if __name__ == "__main__":
    main()
