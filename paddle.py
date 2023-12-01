import pygame as pg


class Paddle:
    def __init__(self, x: int, y: int, width: int, speed: float, max_speed: float):
        self.x = x
        self.y = y
        self.width = width
        self.speed = speed
        self.velocity = 0.0
        self.max_speed = max_speed

    def move(self, direction: int | float, delta_time: float):
        self.velocity += direction * self.speed * delta_time
        self.velocity = max(min(self.velocity, self.max_speed), -self.max_speed)

    def update(self, delta_time: float):
        self.y += self.velocity * delta_time
    def draw(self, screen: pg.Surface):
        pg.draw.rect(screen, (255, 255, 255), (self.x, self.y, 10, self.width))
