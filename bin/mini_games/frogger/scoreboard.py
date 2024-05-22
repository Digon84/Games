from turtle import Turtle

FONT = ("Courier", 20, "normal")


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.level = 1
        self.print_level()

    def print_level(self):
        self.goto(-280, 240)
        self.write(f"Level: {self.level}", align="left", font=FONT)

    def update_level(self):
        self.clear()
        self.level += 1
        self.print_level()

    def game_over(self):
        self.clear()
        self.level = 1
        self.goto(-80, 0)
        self.write("GAME OVER", align="left", font=FONT)

