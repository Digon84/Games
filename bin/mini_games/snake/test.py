from turtle import Screen
from turtle import Turtle

screen = Screen()
screen.tracer(0)
screen.setup(width=600, height=600)
start = (-250, -150)
for i in range(38):
    for j in range(25):
        segment = Turtle("square")
        segment.penup()
        segment.shapesize(stretch_len=0.5, stretch_wid=0.5)
        segment.color("black")
        segment.goto((start[0] + i * 12, start[1] + j * 12))

screen.update()


screen.exitonclick()
