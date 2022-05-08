from __future__ import annotations
import pygame as pg
from vector2d import Vector2D
from car import Car
from boosterType import BoosterType
from stopwatch import Stopwatch


class Booster (pg.sprite.Sprite):
    def __init__(self, position: Vector2D, change: int, type: BoosterType, dt): #change -> wartośc zmiany, jesli dotyczy zmian boolowskich to ==1
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("./data/quick_racing_booster_"+type.value[1]+".png").convert_alpha() # make booster images
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y

        self.type = type
        self.int_booster_value = change
        self.duration = 80

        self.dt = dt #refresh rate -> to use in car

        self.position = position
        self.mask = pg.mask.from_surface(self.image)

    def activate(self, car: Car, stopwatch: Stopwatch):
            if self.type == BoosterType.SPEED:
                car.boosters["speed"] = [self.int_booster_value, pg.time.get_ticks() * self.duration]
                print("SP activated ->", car.boosters)

            elif self.type == BoosterType.TURNING: #turning is smoother/faster or slower
                pass

            elif self.type == BoosterType.NO_COLLISIONS: #the car is "transparent"
                car.boosters["transparent"] = [True, pg.time.get_ticks() * self.duration]
                print("NW activated ->", car.boosters)

            elif self.type == BoosterType.DECREASE_TIMER: #the time of the lap is decreased
                stopwatch.decrease_timer(4000)

            elif self.type == BoosterType.FREEZE:
                car.boosters["freeze"] = [True, pg.time.get_ticks() * self.duration]
                print("FR activated ->", car.boosters)


            else: #BoosterType.NO_TURNING -> self descriptive
                pass

# we gotta find a way to make it last only a short amount of time -> like 3 seconds or so
            
#we can use dt
#we can also add "push" or something - it'd be like booster but with a single push (increase in speed in facing direction)
# -maybe maybe


