from turtle import Turtle
from car import Car

import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10
MAX_Y = 240
MIN_Y = -240


class CarManager(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.move_distance = STARTING_MOVE_DISTANCE
        self.cars = []

    def add_car(self):
        color = random.choice(COLORS)
        starting_point = (280, random.randint(-240, 240))
        self.cars.append(Car(color=color, starting_point=starting_point))

    def move_cars(self):
        for index, car in enumerate(self.cars):
            car.move(self.move_distance)
            if car.xcor() <= -300:
                car.remove()
                self.cars.pop(index)

    def increase_speed(self):
        self.move_distance += MOVE_INCREMENT

    def is_collision(self, x, y):
        for car in self.cars:
            if car.distance(x, y) <= 20 and (abs(car.ycor() - abs(y)) <= 21 or abs(car.ycor() - y) <= 21):
                return True
        return False
