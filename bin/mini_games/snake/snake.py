import os
from enum import Enum
from turtle import Turtle
import time

import pygame

from bin.objects.game_characters import Hero

STARTING_POSITIONS = [(340, 400), (260, 400)]
MOVE_DISTANCE = 60


class Moves(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Snake(Hero):
    def __init__(self):
        self.segments = []
        self.create_snake()

        self.heading = Moves.UP
        snake_image = pygame.image.load('../assets/mini_games/snake/graphics/head.png')
        self.snake_body_image = pygame.image.load('../assets/mini_games/snake/graphics/body.png')
        super().__init__(snake_image, 400, 400, 'snake')

    def create_snake(self):
        for position in STARTING_POSITIONS:
            self.add_segment(position)

    def move(self):
        for seg_num in range(len(self.segments) - 1, -1, -1):
            print(seg_num)
            if seg_num != 0:
                new_x, new_y = self.segments[seg_num - 1]
            else:
                new_x, new_y = self.x, self.y
            self.segments[seg_num] = (new_x, new_y)
        self.move_head()

    def move_head(self):
        if self.heading == Moves.DOWN:
            self.y += MOVE_DISTANCE
        elif self.heading == Moves.UP:
            self.y -= MOVE_DISTANCE
        elif self.heading == Moves.LEFT:
            self.x -= MOVE_DISTANCE
        else:
            self.x += MOVE_DISTANCE

    def add_segment(self, position):
        self.segments.append(position)

    def extend(self):
        self.add_segment(self.segments[-1].position())

    def up(self):
        if self.heading != Moves.DOWN:
            self.heading = Moves.UP

    def down(self):
        if self.heading != Moves.UP:
            self.heading = Moves.DOWN

    def left(self):
        if self.heading != Moves.RIGHT:
            self.heading = Moves.LEFT

    def right(self):
        if self.heading != Moves.LEFT:
            self.heading = Moves.RIGHT
