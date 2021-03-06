from __future__ import annotations


class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, x, y):
        self.x += x
        self.y += y

    def subtract(self, x, y):
        self.x -= x
        self.y -= y

    def subtract_vector(self, other: Vector2D):
        return Vector2D(self.x - other.x, self.y - other.x)

    def add_vector(self, other: Vector2D):
        return Vector2D(self.x + other.x, self.y + other.x)

    def set_y(self, y):
        self.y = y

    def set_x(self, x):
        self.x = x

    def print(self):
        print("x: ", self.x, ", y: ", self.y)
