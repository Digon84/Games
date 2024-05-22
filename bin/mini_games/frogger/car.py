from turtle import Turtle


class Car(Turtle):
    def __init__(self, color, starting_point):
        super().__init__()
        self.starting_point = starting_point
        self.shape("square")
        self.penup()
        self.goto(starting_point)
        self.color(color)
        self.create_car()

    def create_car(self):
        self.resizemode("user")
        self.shapesize(stretch_wid=1, stretch_len=2)
        self.goto(self.starting_point)

    def move(self, distance):
        new_x = self.xcor() - distance
        new_y = self.ycor()
        self.goto(new_x, new_y)

    def remove(self):
        self.reset()
        self.hideturtle()

