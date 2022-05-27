import pygame as pg
from back_elements.map import Map
from math import sin, cos, radians

WHITE = (255, 255, 255)


class Car(pg.sprite.Sprite):
    AIR_RESISTANCE = 0.05
    TURNING_CAPABILITY = 6
    FRONT_BOUNCE = 6
    BACK_BOUNCE = 8
    FRONT_BASE_ACC = 0.1
    BACK_BASE_ACC = 0.03
    MAX_SPEED = 100

    def __init__(self, id, position, speed, direction, rotation, engine, name, curr_map: Map):
        pg.sprite.Sprite.__init__(self)
        self.id = id
        self.name = name
        self.__image = pg.image.load("./data/" + self.name + ".png").convert_alpha()
        self.image = self.__image.copy()
        # self.image.fill((0, 0, 0))
        self.image.set_colorkey(WHITE)  # this will make the img ignore all the white pixels
        self.rect = self.image.get_rect()

        self.position = position
        self.speed = speed
        self.direction = direction
        self.rotation = rotation
        self.engine = engine
        self.map = curr_map

        self.boosters = {"transparent": [False, 0], "speed": [0, 0], "noTurning": [False, 0],
                         "turning": [0, 0], "freeze": [False, 0]}

        self.collision_facilitator = [False, 0]

        self.mask = pg.mask.from_surface(self.image)

        #
        self.nitro_pow = 2  # power
        self.nitro_cap = 60  # capacity
        self.nitro_dur = 40  # duration
        self.nitro_restore = 0.2  # restoration speed

    def update(self, dt):
        self.map.handle_boosters(self)
        self.handle_collision_facilitator()

        # print("speed b4 everything: ", self.speed)

        if self.boosters["freeze"][0]:
            self.speed = 0
        else:
            collision_test_result = self.map.handle_collision_with_walls(self)

            if not collision_test_result[1]:
                self.position.add(self.speed * cos(radians(self.direction)), self.speed * sin(radians(self.direction)))
            else:
                if collision_test_result[0] == "other":
                    if self.speed * (1 + self.boosters["speed"][0]) > 0:
                        self.position.subtract((self.speed * (1 + self.boosters["speed"][0]) + Car.FRONT_BOUNCE) * cos(
                            radians(self.direction)),
                                               (self.speed * (1 + self.boosters["speed"][0]) + Car.FRONT_BOUNCE) * sin(
                                                   radians(self.direction)))
                    else:
                        self.position.add((self.speed * (1 + self.boosters["speed"][0]) + Car.BACK_BOUNCE) * cos(
                            radians(self.direction)),
                                          (self.speed * (1 + self.boosters["speed"][0]) + Car.BACK_BOUNCE) * sin(
                                              radians(self.direction)))

                    self.speed = -(self.speed * (1 + self.boosters["speed"][0])) * Car.AIR_RESISTANCE

                    self.collision_facilitator = [True, pg.time.get_ticks() * 8]

                else:
                    self.boosters["transparent"] = [True, pg.time.get_ticks() * 40]

                # print("Speed after collision: ", self.speed)
                # print("_-----------------------_")

            new_traction = self.map.handle_collision_with_surfaces(self)
            self.map.handle_collision_with_boosters(self)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position.x, self.position.y

        self.mask = pg.mask.from_surface(self.image)

    def move(self, dt):
        pressed = pg.key.get_pressed()
        if pressed[pg.K_SPACE]:
            if self.nitro_dur > 0:
                self.nitro_acc()
                self.nitro_dur -= 1
            else:
                self.nitro_dur = min(self.nitro_dur + self.nitro_restore, self.nitro_cap)
        else:
            self.nitro_dur = min(self.nitro_dur + self.nitro_restore, self.nitro_cap)
        if not self.collision_facilitator[0] and pressed[pg.K_UP]:
            self.accelerate(dt)
        if not self.collision_facilitator[0] and pressed[pg.K_DOWN]:
            self.decelerate(dt)
        if not self.boosters["noTurning"][0]:
            if pressed[pg.K_LEFT]:
                self.rotate_left(dt)
            if pressed[pg.K_RIGHT]:
                self.rotate_right(dt)

        if self.speed > 0:
            # print(self.speed, self.speed * (0.1 + self.speed * 0.01))
            self.speed -= (self.speed * (1 + self.boosters["speed"][0])) * (Car.FRONT_BASE_ACC + (self.speed * (
                        1 + self.boosters["speed"][0])) * 0.15 * Car.AIR_RESISTANCE)  # v drogi i v*v powietrza //static variables -NEEDED!
        elif self.speed < 0:
            self.speed += (self.speed * (1 + self.boosters["speed"][0])) * (
                    Car.BACK_BASE_ACC + (
                        self.speed * (1 + self.boosters["speed"][0])) * Car.AIR_RESISTANCE)  # v drogi i v*v powietrza

        self.speed = min(self.speed, Car.MAX_SPEED)  # so the car doesn't enter "hyperspeed"

    def rotate_left(self, dt):
        if self.speed != 0:
            self.direction = (self.direction - (Car.TURNING_CAPABILITY + self.boosters["turning"][0]) * (
                        self.speed * (1 + self.boosters["speed"][0])) * self.rotation / (
                                      dt ** 2)) % 360

            if self.direction < 0:
                self.direction += 360

            self.image = pg.transform.rotate(self.__image, 360 - self.direction)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = self.position.x, self.position.y
            self.mask = pg.mask.from_surface(self.image)

    def rotate_right(self, dt):
        if self.speed != 0:
            self.direction = (self.direction + (Car.TURNING_CAPABILITY + self.boosters["turning"][0]) * (
                        self.speed * (1 + self.boosters["speed"][0])) * self.rotation / (
                                      dt ** 2)) % 360
            if self.direction > 360:
                self.direction -= 360

            self.image = pg.transform.rotate(self.__image, 360 - self.direction)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = self.position.x, self.position.y

            self.mask = pg.mask.from_surface(self.image)

    def accelerate(self, dt):
        c = min(2, 0.3 + (self.speed / 10) ** 2)
        self.speed += self.engine * c / dt

    def decelerate(self, dt):
        self.speed -= self.engine / (2 * dt)

    def nitro_acc(self):
        self.speed += self.nitro_pow * (lambda x: 1 if x >= 0 else -1)(self.speed)

    def handle_collision_facilitator(self):
        self.collision_facilitator[1] -= pg.time.get_ticks()
        if self.collision_facilitator[1] <= 0:
            self.collision_facilitator[0] = False
            self.collision_facilitator[1] = 0
