import os

import pygame

from bin.objects.game_objects import Collectable
import random


class Food(Collectable):
    def __init__(self, x, y):
        self.COLLECTABLE_WIDTH, self.COLLECTABLE_HEIGHT = 60, 60
        self.image = pygame.image.load(
                os.path.join('../assets/mini_games/pickup_items/graphics/unicorn', 'apple.png'))
        super().__init__(self.image, x, y)

