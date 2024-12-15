from mini_games.draw_a_line.draw_a_line import DrawALine
from mini_games.pickup_items.pickup_items import PickupItems
from mini_games.save_the_xmass.save_the_xmass import SaveTheXmass
from mini_games.frogger.frogger import FroggerGame
from mini_games.snake.main import SnakeGame
from mini_games.garbage_truck_driver.main import GarbageTruckDriver

screen_width = 1200
screen_height = 800

games = [
    {
        'class': DrawALine,
        'name': {'pl': 'RYSOWANIE',
                 'en': 'DRAWING'}
    },
    {
        'class': PickupItems,
        'name': {'pl': 'ZBIERANIE',
                 'en': 'PICKING'}
    },
    {
        'class': SaveTheXmass,
        'name': {'pl': 'URATUJ SWIETA',
                 'en': 'SAVE THE XMASS'}
    },
    # {
    #     'class': FroggerGame,
    #     'name': {'pl': 'FROGGER',
    #              'en': 'FROGGER'}
    # },
    {
        'class': SnakeGame,
        'name': {'pl': 'WAZ',
                 'en': 'SNAKE'}
    },
    # {
    #     'class': GarbageTruckDriver,
    #     'name': {'pl': 'KIEROWCA ŚMIECIARKI',
    #              'en': 'GARBAGE TRUCK DRIVER'}
    # },
]
