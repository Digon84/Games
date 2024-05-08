import os
from itertools import cycle

import pygame

from bin.game import Game
from bin.objects.game_characters import Hero

pygame.display.set_caption("Simple draw line game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 242, 0)
FPS = 60
VEL = 5

COLOR_INDICATION_FRAME = pygame.Rect(1000, 25, 100, 50)
HERO_WIDTH, HERO_HEIGHT = 80, 80
print(os.getcwd())
HERO_IMAGE = pygame.image.load(os.path.join('../assets/mini_games/pickup_items/graphics/unicorn', 'hero.png'))
HERO = pygame.transform.scale(HERO_IMAGE, (HERO_WIDTH, HERO_HEIGHT))
HERO_X_START, HERO_Y_START = 700, 450

POSSIBLE_COLORS = cycle([BLUE, RED, YELLOW, GREEN])

# TODO: remove/change
BORDER_X, BORDER_Y, BORDER_WIDTH, BORDER_HEIGHT = 0, 100, 1200, 800
BORDER = pygame.Rect(BORDER_X, BORDER_Y, BORDER_WIDTH, BORDER_HEIGHT)

class DrawALine(Game):
    def __init__(self, surface, controller):
        self.controller = controller
        border_width, border_height = surface.get_size()
        self.border = pygame.Rect(0, 100, border_width, border_height - 100)
        self.hero = None
        self.chosen_character = None
        self.previous_circles = []
        self.chosen_color = next(POSSIBLE_COLORS)
        super().__init__(surface)

    def init_game(self):
        self.chosen_character = self.chosen_character if self.chosen_character else 'unicorn'
        hero_image = pygame.image.load(
            os.path.join('../assets/mini_games/pickup_items/graphics/unicorn', 'hero.png'))
        self.hero = Hero(hero_image, HERO_X_START, HERO_Y_START, self.chosen_character)

    def start_game(self):
        print("starting draw circles mini-game")
        self.init_game()
        self.draw_window()

    def draw_window(self):
        self.previous_circles.append((self.hero.x + HERO_WIDTH / 2, self.hero.y + HERO_HEIGHT / 2, self.chosen_color))

        self.surface.fill(WHITE)
        pygame.draw.rect(self.surface, WHITE, self.border)
        pygame.draw.rect(self.surface, self.chosen_color, COLOR_INDICATION_FRAME)  # What color to be used to draw
        for i in range(4):
            pygame.draw.rect(self.surface, BLACK, (-i, 100 - i, 1600, 900), 1)
        for x, y, color in self.previous_circles:
            pygame.draw.circle(self.surface, color, center=(x, y), radius=20)
        self.surface.blit(pygame.transform.rotate(HERO, 0), (self.hero.x, self.hero.y))

        pygame.display.update()

    def restart_game(self):
        self.previous_circles = []
        self.hero.x, self.hero.y = HERO_X_START, HERO_Y_START
        self.draw_window()

    def play_game(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.chosen_color = next(POSSIBLE_COLORS)
                    if event.key == pygame.K_DELETE:
                        self.restart_game()
                    if event.key == pygame.K_ESCAPE:
                        run = False
                if event.type == pygame.JOYBUTTONDOWN:
                    if self.controller is not None and self.controller.get_button_values()[0]:
                        self.chosen_color = next(POSSIBLE_COLORS)
                    if self.controller is not None and self.controller.get_button_values()[1]:
                        self.restart_game()
            keys_pressed = pygame.key.get_pressed()
            self.hero_handle_movement(keys_pressed, self.hero)
            if self.controller is not None:
                x, y = self.controller.get_axis_x_y_values()

                self.hero_handle_movement_pad(x, y, self.hero)
            self.draw_window()

        return run

    def hero_handle_movement(self, keys_pressed, hero):
        if keys_pressed[pygame.K_UP]:
            if hero.y - VEL > self.border.y - HERO_HEIGHT / 2:
                hero.y -= VEL
        if keys_pressed[pygame.K_DOWN]:
            if hero.y + VEL < self.border.y + self.border.height - 100 + HERO_HEIGHT / 2:
                hero.y += VEL
        if keys_pressed[pygame.K_LEFT]:
            if hero.x - VEL > self.border.x:
                hero.x -= VEL
        if keys_pressed[pygame.K_RIGHT]:
            if hero.x + VEL < self.border.x + self.border.width - HERO_HEIGHT / 2:
                hero.x += VEL

    def hero_handle_movement_pad(self, x, y, hero):
        if x > 0.5:
            if hero.x + VEL < self.border.x + self.border.width - HERO_HEIGHT / 2:
                hero.x += VEL
        if x < -0.5:
            if hero.x - VEL > self.border.x:
                hero.x -= VEL
        if y > 0.5:
            if hero.y + VEL < self.border.y + self.border.height - 100 + HERO_HEIGHT / 2:
                hero.y += VEL
        if y < -0.5:
            if hero.y - VEL > self.border.y - HERO_HEIGHT / 2:
                hero.y -= VEL
