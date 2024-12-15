import time
from random import randint

import pygame

from bin.game import Game
from bin.mini_games.snake.food import Food
from bin.mini_games.snake.score_board import ScoreBoard
from bin.mini_games.snake.snake import Snake, Moves

FPS = 60


class SnakeGame(Game):
    def __init__(self, surface, controller, update_state):
        self.controller = controller
        self.update_state = update_state
        self.game_over = False
        self.eating = False

        self.border_width, self.border_height = surface.get_size()
        self.border = pygame.Rect(0, 80, self.border_width, self.border_height)
        super().__init__(surface)

    def init_game(self):
        self.score_board = ScoreBoard(self.surface)
        self._place_snake()
        self._place_apple()

    def start_game(self):
        self.init_game()
        self.draw_window()

    def restart_game(self):
        self.start_game()
        self.game_over = False

    def play_game(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        self.update_state('menu')
                    if event.key == pygame.K_SPACE and self.game_over:
                        self.restart_game()
                    if event.key == pygame.K_UP:
                        self.snake.up()
                    if event.key == pygame.K_DOWN:
                        self.snake.down()
                    if event.key == pygame.K_LEFT:
                        self.snake.left()
                    if event.key == pygame.K_RIGHT:
                        self.snake.right()
            if not self.game_over:
                self.snake.move()
                self.handle_apple_collisions()

                if not self.is_snake_in_border():
                    self.game_over = True
                if self.is_head_body_collision():
                    self.game_over = True

            self.draw_window()
            time.sleep(0.4)

    def draw_window(self):
        self.surface.fill('green')
        pygame.draw.rect(self.surface, 'green', self.border)

        # draw apple
        self.surface.blit(pygame.transform.rotate(self.apple.image, 0), (self.apple.x, self.apple.y))

        # draw snake
        for segment_x, segment_y in self.snake.segments:
            self.surface.blit(pygame.transform.rotate(self.snake.snake_body_image, 0), (segment_x, segment_y))
        if self.eating:
            self.surface.blit(pygame.transform.rotate(self.snake.snake_eating_image, 0), (self.snake.x, self.snake.y))
        else:
            self.surface.blit(pygame.transform.rotate(self.snake.image, 0), (self.snake.x, self.snake.y))

        for i in range(21):
            pygame.draw.rect(self.surface, 'black', pygame.Rect(0, 80, i*60, 800), 3, 1)

        for i in range(21):
            pygame.draw.rect(self.surface, 'black', pygame.Rect(0, 80, 1200, i*60), 3, 1)

        self.score_board.write_score()
        if self.game_over:
            self.score_board.game_over()
        pygame.display.update()

    def handle_apple_collisions(self):
        if self.eating:
            self.eating = False
        if self.snake.rect.colliderect(self.apple.rect):
            self._place_apple()
            self.snake.extend()
            self.score_board.increase_score()
            self.eating = True

    def is_head_body_collision(self):
        for snake_segment in self.snake.segments:
            if self.snake.x == snake_segment[0] and self.snake.y == snake_segment[1]:
                return True

        return False

    def is_snake_in_border(self) -> bool:
        head_x, head_y = self.snake.get_head()
        if self.snake.heading == Moves.UP:
            return 80 <= head_y
        elif self.snake.heading == Moves.DOWN:
            return head_y < self.border_height
        elif self.snake.heading == Moves.RIGHT:
            return head_x < self.border_width
        elif self.snake.heading == Moves.LEFT:
            return 0 <= head_x
        else:
            return True

    def _place_snake(self):
        self.snake = Snake()

    def _place_apple(self):
        good_directions = False
        x, y = 0, 0
        while not good_directions:

            x = 60 * randint(0, 19)
            y = 80 + 60 * randint(0, 11)
            for snake_segment in self.snake.segments:
                if (x == snake_segment[0] and y == snake_segment[1]) or (x == self.snake.x and y == self.snake.y):
                    break
            else:
                good_directions = True
                continue
        self.apple = Food(x, y)
