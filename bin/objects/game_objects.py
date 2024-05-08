import pygame

OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 40, 40
COLLECTABLE_WIDTH, COLLECTABLE_HEIGHT = 40, 40


class GameObject:
    def __init__(self, image, start_x, start_y, width, height):
        self.image = pygame.transform.scale(image, (width, height))
        self.x = start_x
        self.y = start_y
        self.width = width
        self.height = height
        self.rect = self.create_rectangle()

    def create_rectangle(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update_coordinates(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y


class Obstacle(GameObject):
    def __init__(self, image, x, y, width=OBSTACLE_WIDTH, height=OBSTACLE_HEIGHT):
        super().__init__(image, x, y, width, height)
        self.can_be_taken = False


class Collectable(GameObject):
    def __init__(self, image, x, y, width=COLLECTABLE_WIDTH, height=COLLECTABLE_HEIGHT):
        super().__init__(image, x, y, width, height)
        self.can_be_taken = True


class MovingObstacle(pygame.sprite.Sprite):
    def __init__(self, images, x, y, obstacle_type=""):
        super().__init__()
        self.frames = []
        self.obstacle_type = obstacle_type
        for image in images:
            self.frames.append(image)

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(x, y))

    def animate(self):
        self.animation_index += 0.1

        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.rect.x -= 3
        self.animate()
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


class EmptySleigh(MovingObstacle):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

    def update(self):
        if self.rect.x >= 500:
            self.rect.x -= 3


class FallingGifts(MovingObstacle):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

    def update(self):
        self.rect.y += 3
        self.destroy()

    def destroy(self):
        if self.rect.y >= 306:
            self.kill()
