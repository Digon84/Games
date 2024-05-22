import pygame.image
import random

from enum import Enum

from bin.game import Game
from bin.objects.game_characters import Santa
from bin.objects.game_objects import MovingObstacle, EmptySleigh, FallingGifts


class GameState(Enum):
    SANTA_RUN = 0
    SANTA_ENTERING_SLEIGHTS = 1
    SLEIGHTS_FLYING_OFF = 2
    SANTA_FLY = 3
    SLEIGHTS_LANDING = 4
    SANTA_AND_HOUSES = 5


class SaveTheXmass(Game):
    def __init__(self, surface, controller, update_state):
        self.backup_window_width, self.backup_window_height = surface.get_size()
        self.window_width, self.window_height = 900, 450
        pygame.display.set_mode((900, 450))
        self.surface = pygame.display.get_surface()
        self.controller = controller
        self.player = None
        self.obstacles = None
        self.collectables = None
        self.houses = None
        self.falling_gifts = None
        self.update_state = update_state
        self.background_sound = pygame.mixer.Sound('../assets/mini_games/save_the_xmass/music/jingle_bells.3gp')
        self.background_sound.set_volume(0.5)
        self.background_sound.play(loops=-1)
        self.pickup_sound = pygame.mixer.Sound('../assets/mini_games/save_the_xmass/music/pickup_sound.mp3')
        self.hit_sound = pygame.mixer.Sound('../assets/mini_games/save_the_xmass/music/hit.mp3')
        self.hit_sound.set_volume(0.4)
        self.run = False

        self.background_animation = 0
        self.game_state = GameState.SANTA_RUN
        self.obstacle_gift_generation_timer = pygame.USEREVENT + 1
        self.animate_player = pygame.USEREVENT + 2
        self.house_generate_timer = pygame.USEREVENT + 3
        self.ground_level = 350
        self.item_generate_time = 1700
        super().__init__(surface)

    def init_game(self):
        pygame.init()
        self.load_surfaces()
        self.player = pygame.sprite.GroupSingle()
        self.obstacles = pygame.sprite.Group()
        self.collectables = pygame.sprite.Group()
        self.houses = pygame.sprite.Group()
        self.falling_gifts = pygame.sprite.Group()

        self.obstacles.add(MovingObstacle([self.tree_surface],
                                          SaveTheXmass.calculate_item_starting_point(), self.ground_level))

        self.player.add(Santa(100, self.ground_level))
        self.draw_window()

    def start_game(self):
        self.init_game()
        pygame.time.set_timer(self.obstacle_gift_generation_timer, self.item_generate_time)
        pygame.time.set_timer(self.animate_player, 10)

    def draw_window(self):
        if self.game_state == GameState.SLEIGHTS_FLYING_OFF:
            self.background_animation += 3
            self.surface.blit(self.background_surface_sky, (0, self.background_animation - self.window_height))
            self.surface.blit(self.background_surface, (0, self.background_animation))
            self.surface.blit(self.ground_surface, (0, self.ground_level + self.background_animation))

        elif self.game_state == GameState.SANTA_FLY:
            self.surface.blit(self.background_surface_sky, (0, 0))
        elif self.game_state == GameState.SLEIGHTS_LANDING:
            self.background_animation += 3
            self.surface.blit(self.background_surface_sky, (0, 0 - self.background_animation))
            self.surface.blit(self.background_surface, (0, self.window_height - self.background_animation))
            self.surface.blit(self.ground_surface, (0, self.window_height + self.ground_level - self.background_animation))
        else:
            self.surface.blit(self.background_surface, (0, 0))
            self.surface.blit(self.ground_surface, (0, self.ground_level))

        self.surface.blit(self.santa_bag_up, (10, 370))
        for i, gift in enumerate(self.player.sprite.gifts):
            self.surface.blit(gift, (20 + i * 60, 380))
        self.surface.blit(self.santa_bag_down, (10, 390))
        self.obstacles.draw(self.surface)
        self.collectables.draw(self.surface)
        self.falling_gifts.draw(self.surface)
        self.houses.draw(self.surface)
        self.player.draw(self.surface)

    def restart_game(self):
        pass

    def play_game(self):
        clock = pygame.time.Clock()
        self.run = True
        while self.run:
            clock.tick(60)
            # print(clock.get_fps())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.finish_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.game_state == GameState.SANTA_AND_HOUSES:
                        gift = self.player.sprite.get_gift()
                        if gift:
                            self.falling_gifts.add(FallingGifts([gift],
                                                                self.player.sprite.rect.center[0]-80,
                                                                self.player.sprite.rect.center[1]))
                    if event.key == pygame.K_ESCAPE:
                        self.finish_game()

                if event.type == self.obstacle_gift_generation_timer:
                    # print("generating obstacle")
                    if self.game_state in [GameState.SANTA_RUN, GameState.SANTA_AND_HOUSES]:
                        # pick flying and ground items
                        selected_object = random.choice(['bird', 'bee', 'tree', 'snow_man', 'gift', 'gift'])
                        if selected_object == 'bird' or selected_object == 'bee':
                            item_y = self.ground_level - 100
                        else:
                            item_y = self.ground_level
                    else:
                        item_y = random.randint(80, self.ground_level)
                        # pick flying items
                        selected_object = random.choice(['bird', 'bee', 'gift', 'gift'])
                        # selected_object = 'gift'
                    if selected_object == 'bee':
                        self.obstacles.add(MovingObstacle(self.bee_surface,
                                                          SaveTheXmass.calculate_item_starting_point(),
                                                          item_y))
                    elif selected_object == 'bird':
                        self.obstacles.add(MovingObstacle(self.bird_surface,
                                                          SaveTheXmass.calculate_item_starting_point(),
                                                          item_y))
                    elif selected_object == 'snow_man':
                        self.obstacles.add(MovingObstacle(self.snow_man_surface,
                                                          SaveTheXmass.calculate_item_starting_point(),
                                                          item_y))
                    elif selected_object == 'tree':
                        self.obstacles.add(MovingObstacle([self.tree_surface],
                                                          SaveTheXmass.calculate_item_starting_point(),
                                                          item_y))
                    elif selected_object == 'gift':
                        gift_choice = random.choice([self.gift_blue_surface,
                                                     self.gift_red_surface,
                                                     self.gift_green_surface])
                        self.collectables.add(MovingObstacle([gift_choice],
                                                             SaveTheXmass.calculate_item_starting_point(),
                                                             item_y))

                if event.type == self.house_generate_timer:
                    house_choice = random.choice([(self.house_red_surface, "house_red_surface"),
                                                  (self.house_yellow_surface, "house_yellow_surface"),
                                                  (self.house_blue_surface, "house_blue_surface")])
                    self.houses.add(MovingObstacle([house_choice[0]],
                                                   SaveTheXmass.calculate_item_starting_point(),
                                                   self.ground_level,
                                                   house_choice[1]))
                if event.type == self.animate_player:
                    self.player.update("animation_update", player_move_type="run")

            self.collision_obstacles()
            self.collision_gifts()
            self.collision_gifts_and_houses()
            self.handle_game_states()
            self.obstacles.update()
            self.collectables.update()
            self.houses.update()
            self.falling_gifts.update()
            self.player.update()
            self.draw_window()
            pygame.display.update()

    def finish_game(self):
        pygame.display.set_mode((self.backup_window_width, self.backup_window_height))
        self.background_sound.stop()
        self.update_state('menu')
        self.run = False

    def collision_obstacles(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.obstacles, True):
            if self.game_state == GameState.SANTA_ENTERING_SLEIGHTS:
                self.player.update("player_move_type", player_move_type="fly")
                self.game_state = GameState.SLEIGHTS_FLYING_OFF
            else:
                self.hit_sound.play()
                self.player.sprite.set_hit()
        else:
            pass

    def collision_gifts(self):
        colliding_sprites = pygame.sprite.spritecollide(self.player.sprite, self.collectables, True)
        if colliding_sprites:
            if self.game_state == GameState.SANTA_RUN or GameState.SANTA_FLY:
                for colliding in colliding_sprites:
                    self.player.update("collected_gifts", gift=colliding.image)
                    self.pickup_sound.play()

    def collision_gifts_and_houses(self):
        if self.game_state == GameState.SANTA_AND_HOUSES:
            colliding_sprites = pygame.sprite.groupcollide(self.falling_gifts, self.houses, True, False)
            if colliding_sprites:
                for colliding_houses in colliding_sprites.values():
                    for colliding_house in colliding_houses:
                        if colliding_house.obstacle_type == "house_red_surface":
                            colliding_house.frames = [self.house_red_lights_surface]
                        elif colliding_house.obstacle_type == "house_yellow_surface":
                            colliding_house.frames = [self.house_yellow_lights_surface]
                        elif colliding_house.obstacle_type == "house_blue_surface":
                            colliding_house.frames = [self.house_blue_lights_surface]

    def handle_game_states(self):
        gifts_collected = self.player.sprite.gift_amount
        if self.game_state == GameState.SANTA_RUN and gifts_collected >= 5:
            pygame.time.set_timer(self.obstacle_gift_generation_timer, 0)
            self.collectables.empty()
            self.obstacles.empty()
            self.obstacles.add(EmptySleigh([self.sleigh_surface],
                                           SaveTheXmass.calculate_item_starting_point(), self.ground_level))
            self.game_state = GameState.SANTA_ENTERING_SLEIGHTS
        elif self.game_state == GameState.SANTA_FLY and gifts_collected >= 10:
            pygame.time.set_timer(self.obstacle_gift_generation_timer, 0)
            self.game_state = GameState.SLEIGHTS_LANDING
            self.background_animation = 0
            self.collectables.empty()
            self.obstacles.empty()
        elif self.game_state == GameState.SLEIGHTS_FLYING_OFF and self.background_animation >= self.window_height:
            self.game_state = GameState.SANTA_FLY
            pygame.time.set_timer(self.obstacle_gift_generation_timer, self.item_generate_time)
        elif self.game_state == GameState.SLEIGHTS_LANDING and self.background_animation >= self.window_height:
            self.game_state = GameState.SANTA_AND_HOUSES
            self.background_animation = 0
            pygame.time.set_timer(self.house_generate_timer, self.item_generate_time + 1000)
        elif self.game_state == GameState.SANTA_AND_HOUSES:
            if self.player.sprite.gift_amount == 0 and not self.falling_gifts:
                print("Game End")

    def load_surfaces(self):
        self.background_surface = pygame.image.load('../assets/mini_games/save_the_xmass/graphics/background.png').convert()
        self.background_surface_sky = pygame.image.load('../assets/mini_games/save_the_xmass/graphics/background_sky.png').convert()
        self.ground_surface = pygame.image.load('../assets/mini_games/save_the_xmass/graphics/ground.png').convert()
        self.santa_bag_up = pygame.image.load('../assets/mini_games/save_the_xmass/graphics/santa_bag_up.png').convert_alpha()
        self.santa_bag_down = pygame.image.load('../assets/mini_games/save_the_xmass/graphics/santa_bag_down.png').convert_alpha()
        self.background_surface = pygame.image.load('../assets/mini_games/save_the_xmass/graphics/background.png').convert()
        self.bee_surface = [pygame.image.load('../assets/mini_games/save_the_xmass/graphics/obstacles/bee1.png').convert_alpha(),
                            pygame.image.load('../assets/mini_games/save_the_xmass/graphics/obstacles/bee2.png').convert_alpha()]
        self.tree_surface = pygame.image.load('../assets/mini_games/save_the_xmass/graphics/obstacles/tree.png').convert_alpha()
        self.snow_man_surface = [pygame.image.load('../assets/mini_games/save_the_xmass/graphics/obstacles/snow_man.png').convert_alpha(),
                                 pygame.image.load('../assets/mini_games/save_the_xmass/graphics/obstacles/snow_man2.png').convert_alpha(),
                                 pygame.image.load('../assets/mini_games/save_the_xmass/graphics/obstacles/snow_man3.png').convert_alpha(),
                                 pygame.image.load('../assets/mini_games/save_the_xmass/graphics/obstacles/snow_man4.png').convert_alpha(),
                                 pygame.image.load('../assets/mini_games/save_the_xmass/graphics/obstacles/snow_man5.png').convert_alpha(),
                                 pygame.image.load('../assets/mini_games/save_the_xmass/graphics/obstacles/snow_man6.png').convert_alpha()]
        self.bird_surface = [pygame.image.load('../assets/mini_games/save_the_xmass/graphics/obstacles/bird1.png').convert_alpha(),
                             pygame.image.load('../assets/mini_games/save_the_xmass/graphics/obstacles/bird2.png').convert_alpha(),
                             pygame.image.load('../assets/mini_games/save_the_xmass/graphics/obstacles/bird3.png').convert_alpha(),
                             pygame.image.load('../assets/mini_games/save_the_xmass/graphics/obstacles/bird4.png').convert_alpha(),
                             pygame.image.load('../assets/mini_games/save_the_xmass/graphics/obstacles/bird5.png').convert_alpha(),
                             pygame.image.load('../assets/mini_games/save_the_xmass/graphics/obstacles/bird6.png').convert_alpha(),
                             pygame.image.load('../assets/mini_games/save_the_xmass/graphics/obstacles/bird7.png').convert_alpha(),
                             pygame.image.load('../assets/mini_games/save_the_xmass/graphics/obstacles/bird8.png').convert_alpha()]
        self.gift_blue_surface = pygame.image.load(f'../assets/mini_games/save_the_xmass/graphics/pickable/gift_blue.png').convert_alpha()
        self.gift_red_surface = pygame.image.load(f'../assets/mini_games/save_the_xmass/graphics/pickable/gift_red.png').convert_alpha()
        self.gift_green_surface = pygame.image.load(f'../assets/mini_games/save_the_xmass/graphics/pickable/gift_green.png').convert_alpha()
        self.sleigh_surface = pygame.image.load('../assets/mini_games/save_the_xmass/graphics/sleigh/empty/sleigh_empty.png').convert_alpha()
        self.house_red_surface = pygame.image.load('../assets/mini_games/save_the_xmass/graphics/houses/house_red.png').convert_alpha()
        self.house_blue_surface = pygame.image.load('../assets/mini_games/save_the_xmass/graphics/houses/house_blue.png').convert_alpha()
        self.house_yellow_surface = pygame.image.load('../assets/mini_games/save_the_xmass/graphics/houses/house_yellow.png').convert_alpha()
        self.house_red_lights_surface = pygame.image.load(
            '../assets/mini_games/save_the_xmass/graphics/houses/house_red_lights.png').convert_alpha()
        self.house_blue_lights_surface = pygame.image.load(
            '../assets/mini_games/save_the_xmass/graphics/houses/house_blue_lights.png').convert_alpha()
        self.house_yellow_lights_surface = pygame.image.load(
            '../assets/mini_games/save_the_xmass/graphics/houses/house_yellow_lights.png').convert_alpha()

    @staticmethod
    def calculate_item_starting_point():
        return random.randint(1000, 1200)
