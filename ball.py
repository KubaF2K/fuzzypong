import random
import math
import pygame as pg


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

    def draw(self, screen: pg.Surface):
        pg.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius)
