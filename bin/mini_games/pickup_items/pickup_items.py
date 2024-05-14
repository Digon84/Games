import pygame
from random import choice, randint
import os

from bin.game import Game
from bin.objects.game_objects import Collectable
from bin.objects.game_characters import Hero

DEBUG = False

CHARACTERS = {
    'unicorn': {
        'files_location': os.path.join('..', 'assets', 'mini_games', 'pickup_items', 'graphics', 'unicorn'),
        'collectables': ['apple', 'carrot', 'water-bucket'],
        'obstacles': ['stone']
    },
    'santa': {
        'files_location': os.path.join('..', 'assets', 'mini_games', 'pickup_items', 'graphics', 'santa'),
        'collectables': ['car', 'ball', 'cookie', 'doll', 'bear'],
        'obstacles': ['stone']
    },
    'paw_patrol': {
        'files_location': os.path.join('..', 'assets', 'mini_games', 'pickup_items', 'graphics', 'paw_patrol'),
        'collectables': ['chase', 'everest', 'marshal', 'rubble', 'sky', 'zuma'],
        'obstacles': ['stone']
    }
}
WIDTH, HEIGHT = 1600, 900
HERO_X_START, HERO_Y_START = 700, 450

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
VEL = 5


class PickupItems(Game):
    def __init__(self, surface, controller, update_state):
        self.controller = controller
        self.heroes_to_chose = []
        self.chosen_character = None
        self.files_location = None
        self.hero = None
        self.collectables = None
        self.obstacles = None
        self.menu_choice = None
        self.update_state = update_state
        border_width, border_height = surface.get_size()
        self.border = pygame.Rect(0, 100, border_width, border_height - 100)

        pygame.display.set_caption("Pick up simple game")
        super().__init__(surface)

    def init_game(self):
        self.heroes_to_chose = []
        self.chosen_character = self.chosen_character if self.chosen_character else 'unicorn'

        self._generate_hero_menu()
        self.files_location = CHARACTERS[self.chosen_character]['files_location']

        hero_image = pygame.image.load(
            os.path.join(self.files_location, 'hero.png'))
        self.hero = Hero(hero_image, HERO_X_START, HERO_Y_START, self.chosen_character)

        self.collectables = self._generate_collectables()
        self.obstacles = self._generate_obstacles()

    def start_game(self):
        print("starting pick up items mini-game")
        self.init_game()
        self.draw_window()

    def restart_game(self):
        self.init_game()
        self.draw_window()

    def play_game(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DELETE:
                        self.restart_game()
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        self.update_state('menu')
                if event.type == pygame.JOYBUTTONDOWN:
                    if self.controller.get_button_values()[1]:
                        self.restart_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.menu_choice = self.get_menu_collision()
                    if self.menu_choice:
                        self.chosen_character = self.menu_choice.character_type
                        self.restart_game()

            keys_pressed = pygame.key.get_pressed()
            self.hero_handle_movement(keys_pressed, self.hero)
            if self.controller is not None:
                x, y = self.controller.get_axis_x_y_values()
                self.hero_handle_movement_pad(x, y, self.hero)
            self.handle_collectables_collisions()
            self.menu_choice = self.get_menu_collision()
            self.draw_window()
        return run

    def get_menu_collision(self):
        point = pygame.mouse.get_pos()
        for hero_to_chose in self.heroes_to_chose:
            collide = hero_to_chose.rect.collidepoint(point)
            if collide:
                return hero_to_chose
        else:
            return None

    def handle_collectables_collisions(self):
        remaining_collectables = []
        for collectable in self.collectables:
            if collectable.rect.colliderect(self.hero.rect):
                collectable.update_coordinates(10 + 40 * len(self.hero.collected_items), 30)
                self.hero.collected_items.append(collectable)
            else:
                remaining_collectables.append(collectable)

        self.collectables = remaining_collectables

    def hero_handle_movement_pad(self, x, y, hero):
        x_change = 0
        y_change = 0
        if x > 0.5:
            if hero.x + VEL < self.border.x + self.border.width - 35 - hero.height / 2:
                x_change = VEL
        if x < -0.5:
            if hero.x - VEL > self.border.x - 5:
                x_change = -VEL
        if y > 0.5:
            if hero.y + VEL < self.border.y + self.border.height - 115 + hero.height / 2:
                y_change = VEL
        if y < -0.5:
            if hero.y - VEL > self.border.y + 40 - hero.height / 2:
                y_change = -VEL
        hero.update_coordinates(hero.x + x_change, hero.y + y_change)

    def hero_handle_movement(self, keys_pressed, hero):
        x_change = 0
        y_change = 0
        if keys_pressed[pygame.K_UP]:
            if hero.y - VEL > self.border.y + 40 - hero.height / 2:
                y_change = -VEL
        if keys_pressed[pygame.K_DOWN]:
            if hero.y + VEL < self.border.y + self.border.height - 115 + hero.height / 2:
                y_change = VEL
        if keys_pressed[pygame.K_LEFT]:
            if hero.x - VEL > self.border.x - 5:
                x_change = -VEL
        if keys_pressed[pygame.K_RIGHT]:
            if hero.x + VEL < self.border.x + self.border.width - 35 - hero.height / 2:
                x_change = VEL
        hero.update_coordinates(hero.x + x_change, hero.y + y_change)

    def draw_window(self):
        self.surface.fill(WHITE)
        pygame.draw.rect(self.surface, WHITE, self.border)
        pygame.draw.rect(self.surface, BLACK, (0, 100, 1600, 5), 3)

        # TODO: remove obstacles for now. Use it later
        # for game_object in [*collectables, *obstacles, hero]:
        for game_object in [*self.collectables, self.hero, *self.heroes_to_chose]:
            self.surface.blit(pygame.transform.rotate(game_object.image, 0), (game_object.x, game_object.y))

        for i, picked_up_collectable in enumerate(self.hero.collected_items):
            self.surface.blit(pygame.transform.rotate(picked_up_collectable.image, 0),
                              (picked_up_collectable.x, picked_up_collectable.y))

        if self.menu_choice:
            pygame.draw.rect(self.surface, BLACK, self.menu_choice.rect, 3, 1)

        if DEBUG:
            for game_object in [*self.collectables, self.hero]:
                pygame.draw.rect(self.surface, BLACK, game_object.rect, 3, 1)

        pygame.display.update()

    def _generate_hero_menu(self):
        for i, key in enumerate(CHARACTERS.keys()):
            hero_image = pygame.image.load(
                os.path.join(CHARACTERS[key]['files_location'], 'hero.png'))
            width, _ = self.surface.get_size()
            self.heroes_to_chose.append(Hero(hero_image, width - 100 - 100 * i, 10, key))

    def _generate_collectables(self):
        collectables = CHARACTERS[self.chosen_character]['collectables']
        generated_objects = []
        while len(generated_objects) != 10:
            collectable = choice(collectables)
            collectable_image = pygame.image.load(
                os.path.join(self.files_location, collectable + '.png'))
            x = randint(self.border.x, self.border.width - 40)
            y = randint(self.border.y, self.border.height - 40)
            collectable_obj = Collectable(collectable_image, x, y)

            if collectable_obj.rect.colliderect(self.hero.rect):
                continue
            if generated_objects:
                for existing_obj in generated_objects:
                    if collectable_obj.rect.colliderect(existing_obj.rect):
                        break
                else:
                    generated_objects.append(collectable_obj)
            else:
                generated_objects.append(collectable_obj)

        return generated_objects

    def _generate_obstacles(self):
        c = []
        obstacles = CHARACTERS[self.chosen_character]['obstacles']
        for i in range(4):
            obstacle = choice(obstacles)
            collectable_image = pygame.image.load(
                os.path.join(self.files_location, obstacle + '.png'))
            x = randint(self.border.x, self.border.width - 40)
            y = randint(self.border.y, self.border.height - 40)
            c.append(Collectable(collectable_image, x, y))
        return c
