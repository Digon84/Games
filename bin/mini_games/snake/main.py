# from turtle import Screen
# import time
import time

import pygame
#
# from food import Food
# from score_board import ScoreBoard
# from snake import Snake
from bin.game import Game
from bin.mini_games.snake.food import Food
from bin.mini_games.snake.snake import Snake

FPS = 60


class SnakeGame(Game):
    def __init__(self, surface, controller, update_state):
        self.controller = controller
        self.update_state = update_state

        border_width, border_height = surface.get_size()
        self.border = pygame.Rect(0, 100, border_width, border_height)
        super().__init__(surface)

    def init_game(self):
        self._place_snake()
        self._place_apple()

    def start_game(self):
        self.init_game()
        self.draw_window()

    def restart_game(self):
        pass

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

            self.snake.move()
            self.draw_window()
            time.sleep(0.5)

    def draw_window(self):
        self.surface.fill('green')
        pygame.draw.rect(self.surface, 'green', self.border)

        # draw apple
        self.surface.blit(pygame.transform.rotate(self.apple.image, 0), (self.apple.x, self.apple.y))

        # draw snake
        for segment_x, segment_y in self.snake.segments:
            self.surface.blit(pygame.transform.rotate(self.snake.snake_body_image, 0), (segment_x, segment_y))
        self.surface.blit(pygame.transform.rotate(self.snake.image, 0), (self.snake.x, self.snake.y))


        pygame.display.update()

    def _place_snake(self):
        self.snake = Snake()

    def _place_apple(self):
        self.apple = Food(10, 10)

#
# screen = Screen()
# screen.setup(width=600, height=600)
# screen.bgcolor("black")
# screen.title("Snake Game")
# screen.tracer(0)
#
# snake = Snake(screen)
# food = Food()
# score_board = ScoreBoard()
#
# screen.listen()
# screen.onkey(snake.up, "Up")
# screen.onkey(snake.down, "Down")
# screen.onkey(snake.left, "Left")
# screen.onkey(snake.right, "Right")
#
# game_is_on = True
# while game_is_on:
#     screen.update()
#     time.sleep(0.1)
#     snake.move()
#
#     if snake.head.distance(food) < 15:
#         food.refresh()
#         snake.extend()
#         score_board.update_score()
#
#     if snake.head.xcor() > 280 or snake.head.xcor() < -280 or snake.head.ycor() > 280 or snake.head.ycor() < -280:
#         game_is_on = False
#         score_board.game_over()
#
#     for segment in snake.segments[1:]:
#         if snake.head.distance(segment) < 10:
#             game_is_on = False
#             score_board.game_over()
#
# screen.exitonclick()
