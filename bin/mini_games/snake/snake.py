import os
from enum import Enum
from turtle import Turtle
import time

import pygame

from bin.objects.game_characters import Hero

STARTING_POSITIONS = [(480, 380), (420, 380)]
MOVE_DISTANCE = 60


class Moves(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Snake(Hero):
    def __init__(self):
        self.CHARACTER_WIDTH = 60
        self.CHARACTER_HEIGHT = 60
        self.segments = []
        self.create_snake()
        self.heading = None
        snake_image = pygame.image.load('../assets/mini_games/snake/graphics/head.png')
        self.snake_body_image = pygame.transform.scale(
            pygame.image.load('../assets/mini_games/snake/graphics/body.png'),
            (self.CHARACTER_WIDTH, self.CHARACTER_HEIGHT))
        self.snake_eating_image = pygame.transform.scale(
            pygame.image.load('../assets/mini_games/snake/graphics/head_eating.png'),
            (self.CHARACTER_WIDTH, self.CHARACTER_HEIGHT))
        super().__init__(snake_image, 540, 380, 'snake')

    def create_snake(self):
        for position in STARTING_POSITIONS:
            self.add_segment(position)

    def move(self):
        if self.heading is not None:
            for seg_num in range(len(self.segments) - 1, -1, -1):
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
        elif self.heading == Moves.RIGHT:
            self.x += MOVE_DISTANCE
        self.update_coordinates(self.x, self.y)

    def get_head(self):
        return self.x, self.y

    def add_segment(self, position):
        self.segments.append(position)

    def extend(self):
        self.add_segment(self.segments[-1])

    def up(self):
        if self.heading != Moves.DOWN:
            self.heading = Moves.UP

    def down(self):
        if self.heading != Moves.UP:
            self.heading = Moves.DOWN

    def left(self):
        if self.heading != Moves.RIGHT and self.heading is not None:
            self.heading = Moves.LEFT

    def right(self):
        if self.heading != Moves.LEFT:
            self.heading = Moves.RIGHT
