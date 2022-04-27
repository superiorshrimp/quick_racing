import pygame as pg
from vector2d import Vector2D
from math import sin, cos, radians

WHITE = (255, 255, 255)


class Car(pg.sprite.Sprite):
    def __init__(self, id, position, speed, direction, rotation, engine):
        pg.sprite.Sprite.__init__(self)
        self.__image = pg.image.load("./data/supra_new.png").convert_alpha()
        self.image = self.__image.copy()
        # self.image.fill((0, 0, 0))
        self.image.set_colorkey(WHITE)  # this will make the img ignore all the white pixels
        self.rect = self.image.get_rect()
        self.rect.center = (position.x, position.y)
        self.name = "Car"

        self.id = id
        self.position = position
        self.speed = speed
        self.direction = direction
        self.rotation = rotation
        self.engine = engine

    def update(self, dt):
        pressed = pg.key.get_pressed()
        if pressed[pg.K_UP]:
            self.accelerate(dt)
        if pressed[pg.K_DOWN]:
            self.decelerate(dt)
        if pressed[pg.K_LEFT]:
            self.rotate_left(dt)
        if pressed[pg.K_RIGHT]:
            self.rotate_right(dt)

    def move(self, dt):
        if self.speed > 0:
            print(self.speed, self.speed * (0.1 + self.speed * 0.01))
            self.speed -= self.speed * (0.1 + self.speed * 0.01)  # v drogi i v*v powietrza
        elif self.speed < 0:
            self.speed += self.speed * (0.03 + self.speed * 0.05)  # v drogi i v*v powietrza
        self.position.add(self.speed * cos(radians(self.direction)), self.speed * sin(radians(self.direction)))
        self.rect.x = self.position.x
        self.rect.y = self.position.y

        # if self.rect.left > 400: #for now hardcoded
        #     self.rect.right = 0

    # def collision(self, wall):
    #    self.direction += 180 - abs(self.direction - wall.get_facing)

    def rotate_left(self, dt):
        if self.speed != 0:
            self.direction -= 3 * self.speed * self.rotation / (dt ** 2)
            if self.direction < 0:
                self.direction += 360
            self.image = pg.transform.rotate(self.__image, 360 - self.direction)

    def rotate_right(self, dt):
        if self.speed != 0:
            self.direction += 3 * self.speed * self.rotation / (dt ** 2)
            if self.direction > 360:
                self.direction -= 360
            self.image = pg.transform.rotate(self.__image, 360 - self.direction)

    def accelerate(self, dt):
        self.speed += self.engine / dt

    def decelerate(self, dt):
        self.speed -= self.engine / (2 * dt)


