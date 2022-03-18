import pygame as pg
from vector2d import Vector2D
from car import Car
from map import Map
from wall import Wall

class Engine:
    def __init__(self, refresh_rate):
        self.refresh = refresh_rate
        pg.init()
        self.screen = pg.display.set_mode((400,300))
        pg.display.update()
        pg.display.set_caption("QUICK RACING")
        self.clock = pg.time.Clock()

    def run(self):
        wall1 = Wall(Vector2D(20, 100), Vector2D(20, 80))
        car = Car(0, Vector2D(10,10), 0, 0, 60, 30)
        car_img = pg.image.load("./data/car.png")
        map = Map(0, 1000, 300, car, [wall1])
        map_img = pg.image.load("./data/grass.png")
        run = True

        while run:
            dt = self.clock.tick(self.refresh)
            self.screen.blit(map_img, (0, 0))
            self.screen.blit(car_img, (car.position.x, car.position.y))
            pg.draw.rect(self.screen,(0,0,0),[20,20,20,20])
            
            pressed = pg.key.get_pressed()
            if pressed[pg.K_UP]:
                car.accelerate(dt)
            if pressed[pg.K_DOWN]:
                car.decelerate(dt)
            if pressed[pg.K_LEFT]:
                car.rotate_left(dt)
            if pressed[pg.K_RIGHT]:
                car.rotate_right(dt)

            map.collision_test()
            car.move(dt)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
            pg.display.flip()
    
def main():
    engine = Engine(60)
    engine.run()

if __name__ == "__main__":
    main()