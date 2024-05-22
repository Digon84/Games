import pygame.sprite

from bin.objects.game_objects import GameObject

CHARACTER_WIDTH, CHARACTER_HEIGHT = 80, 80


class Character(GameObject):
    def __init__(self, image, x, y, character_type, width=CHARACTER_WIDTH, height=CHARACTER_HEIGHT):
        super().__init__(image, x, y, width, height)
        self.character_type = character_type


class Hero(Character):
    def __init__(self, image, x, y, character_type):
        super().__init__(image, x, y, character_type)
        self.collected_items = []


class Santa(pygame.sprite.Sprite):
    MOVE_SPEED = 3

    def __init__(self, x, y):
        super().__init__()
        self.run_frames = []
        self.fly_frames = []
        self.idle_frames = []
        self.hit_frames = []
        self.hit_fly_frames = []
        self.jump_frames = []
        self.animation_index = 0
        self.hit_status = False
        self.jump_sound = pygame.mixer.Sound('../assets/mini_games/save_the_xmass/music/jump.mp3')
        self.jump_sound.set_volume(0.5)

        self.gifts = []
        self.gift_amount = len(self.gifts)
        self.previous_movement = "idle"
        self.player_move_type = "run"
        self.load_frames()

        if self.player_move_type == "run":
            self.image = self.run_frames[self.animation_index]
        else:
            self.image = self.fly_frames[self.animation_index]

        self.rect = self.image.get_rect(midbottom=(x, y))
        self.gravity = 0
        self.ground_level = y

    def load_frames(self):
        self.load_hit_frames()
        self.load_fly_hit_frames()
        self.load_run_frames()
        self.load_idle_frames()
        self.load_jump_frames()
        self.load_fly_frames()

    def load_fly_frames(self):
        fly_images = ['../assets/mini_games/save_the_xmass/graphics/santa/flying/fly/fly1.png']
        for image in fly_images:
            frame = pygame.image.load(image).convert_alpha()
            self.fly_frames.append(frame)

    def load_jump_frames(self):
        jump_images = ['../assets/mini_games/save_the_xmass/graphics/santa/running/jump/jump1.png',
                       '../assets/mini_games/save_the_xmass/graphics/santa/running/jump/jump2.png',
                       '../assets/mini_games/save_the_xmass/graphics/santa/running/jump/jump3.png',
                       '../assets/mini_games/save_the_xmass/graphics/santa/running/jump/jump4.png']
        for image in jump_images:
            frame = pygame.image.load(image).convert_alpha()
            self.jump_frames.append(frame)

    def load_idle_frames(self):
        idle_images = ['../assets/mini_games/save_the_xmass/graphics/santa/running/idle/idle1.png',
                       '../assets/mini_games/save_the_xmass/graphics/santa/running/idle/idle2.png',
                       '../assets/mini_games/save_the_xmass/graphics/santa/running/idle/idle3.png',
                       '../assets/mini_games/save_the_xmass/graphics/santa/running/idle/idle4.png',
                       '../assets/mini_games/save_the_xmass/graphics/santa/running/idle/idle5.png',
                       '../assets/mini_games/save_the_xmass/graphics/santa/running/idle/idle6.png']
        for image in idle_images:
            frame = pygame.image.load(image).convert_alpha()
            self.idle_frames.append(frame)

    def load_run_frames(self):
        run_images = ['../assets/mini_games/save_the_xmass/graphics/santa/running/run/run1.png',
                      '../assets/mini_games/save_the_xmass/graphics/santa/running/run/run2.png',
                      '../assets/mini_games/save_the_xmass/graphics/santa/running/run/run3.png',
                      '../assets/mini_games/save_the_xmass/graphics/santa/running/run/run4.png',
                      '../assets/mini_games/save_the_xmass/graphics/santa/running/run/run5.png',
                      '../assets/mini_games/save_the_xmass/graphics/santa/running/run/run6.png']
        for image in run_images:
            frame = pygame.image.load(image).convert_alpha()
            self.run_frames.append(frame)

    def load_hit_frames(self):
        hit_images = ['../assets/mini_games/save_the_xmass/graphics/santa/running/hit/hit1.png',
                      '../assets/mini_games/save_the_xmass/graphics/santa/running/hit/hit2.png',
                      '../assets/mini_games/save_the_xmass/graphics/santa/running/hit/hit3.png']
        for image in hit_images:
            frame = pygame.image.load(image).convert_alpha()
            self.hit_frames.append(frame)

    def load_fly_hit_frames(self):
        hit_fly_images = ['../assets/mini_games/save_the_xmass/graphics/santa/flying/hit/hit1.png',
                          '../assets/mini_games/save_the_xmass/graphics/santa/flying/hit/hit2.png',
                          '../assets/mini_games/save_the_xmass/graphics/santa/flying/hit/hit3.png']
        for image in hit_fly_images:
            frame = pygame.image.load(image).convert_alpha()
            self.hit_fly_frames.append(frame)

    def player_input(self):
        keys = pygame.key.get_pressed()
        self.previous_movement = "idle"
        if keys[pygame.K_SPACE] and self.rect.bottom >= self.ground_level and self.player_move_type == "run":
            self.jump_sound.play()
            self.gravity = -20
        if keys[pygame.K_LEFT] and self.rect.left >= 0:
            self.previous_movement = "run"
            self.rect.x -= self.MOVE_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right <= 900:
            self.rect.x += self.MOVE_SPEED
            self.previous_movement = "run"
        if keys[pygame.K_UP] and self.rect.top >= 0 and self.player_move_type == "fly":
            self.rect.y -= self.MOVE_SPEED
            self.previous_movement = "run"
        if keys[pygame.K_DOWN] and self.rect.bottom <= self.ground_level and self.player_move_type == "fly":
            self.rect.y += self.MOVE_SPEED
            self.previous_movement = "run"

        if self.hit_status:
            self.previous_movement = "hit"

    def apply_gravity(self):
        if self.player_move_type == "run":
            self.gravity += 1
            self.rect.y += self.gravity
            if self.rect.bottom >= self.ground_level:
                self.rect.bottom = self.ground_level

    def animate_player(self):
        self.animation_index += 0.1

        if self.player_move_type == "run":
            if self.previous_movement == "hit":
                if self.animation_index >= len(self.hit_frames):
                    self.animation_index = 0
                    self.hit_status = False
                self.image = self.hit_frames[int(self.animation_index)]
            elif self.previous_movement == "idle":
                if self.rect.bottom < self.ground_level:
                    if self.animation_index >= len(self.jump_frames):
                        self.animation_index = len(self.jump_frames) - 1
                    self.image = self.jump_frames[int(self.animation_index)]
                else:
                    if self.animation_index >= len(self.idle_frames):
                        self.animation_index = 0
                    self.image = self.idle_frames[int(self.animation_index)]
            elif self.previous_movement == "run":
                if self.rect.bottom < self.ground_level:
                    if self.animation_index >= len(self.jump_frames):
                        self.animation_index = len(self.jump_frames) - 1
                    self.image = self.jump_frames[int(self.animation_index)]
                else:
                    if self.animation_index >= len(self.run_frames):
                        self.animation_index = 0
                    self.image = self.run_frames[int(self.animation_index)]
        else:
            if self.previous_movement == "hit":
                if self.animation_index >= len(self.hit_fly_frames):
                    self.animation_index = 0
                    self.hit_status = False
                self.image = self.hit_fly_frames[int(self.animation_index)]
            elif self.previous_movement == "idle":
                if self.animation_index >= len(self.fly_frames):
                    self.animation_index = 0
                self.image = self.fly_frames[int(self.animation_index)]
            elif self.previous_movement == "run":
                if self.animation_index >= len(self.fly_frames):
                    self.animation_index = 0
                self.image = self.fly_frames[int(self.animation_index)]

    def update(self, update_type="", player_move_type="run", ground_level_modifier=0, gift=None):
        if update_type == "animation_update":
            self.animate_player()
        elif update_type == "player_move_type":
            self.player_move_type = player_move_type
            if self.player_move_type == "run":
                x = 120
                self.image = self.run_frames[0]
            else:
                x = 500
                self.image = self.fly_frames[0]
            self.rect = self.image.get_rect(bottomleft=(x, self.ground_level))
        elif update_type == "ground_level":
            self.ground_level += ground_level_modifier
        elif update_type == "collected_gifts":
            if gift is not None:
                self.gifts.append(gift)
                self.gift_amount = len(self.gifts)
        else:
            self.player_input()
            self.apply_gravity()

    def get_gift(self):
        if self.gifts:
            gift = self.gifts.pop()
            self.gift_amount = len(self.gifts)
            return gift

    def set_hit(self):
        self.animation_index = 0
        self.hit_status = True
        self.previous_movement = "hit"
