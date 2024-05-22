# import random
# import time
# from turtle import Screen
# from player import Player
# from car_manager import CarManager
# from scoreboard import Scoreboard
from bin.game import Game


class FroggerGame(Game):
    def __init__(self, surface, controller, update_state):
        super().__init__(surface)

    def init_game(self):
        pass

    def start_game(self):
        pass

    def restart_game(self):
        pass

    def play_game(self):
        pass



# screen = Screen()
# screen.setup(width=600, height=600)
# screen.tracer(0)
# screen.listen()
#
# player = Player()
# score_board = Scoreboard()
# car_manager = CarManager()
#
# game_is_on = True
# while game_is_on:
#     time.sleep(0.1)
#     screen.update()
#     screen.onkey(player.move_forward, "Up")
#     if random.randint(0, 10) > 8:
#         car_manager.add_car()
#     car_manager.move_cars()
#
#     if player.ycor() >= 280:
#         # level up, reset player
#         player.reset_position()
#         score_board.update_level()
#         car_manager.increase_speed()
#
#     if car_manager.is_collision(player.xcor(), player.ycor()):
#         score_board.game_over()
#         game_is_on = False
#
# screen.exitonclick()
