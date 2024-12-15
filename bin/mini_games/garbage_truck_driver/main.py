import pygame

from bin.game import Game

FPS = 60


class GarbageTruckDriver(Game):
    def __init__(self, surface, controller, update_state):
        self.controller = controller
        self.update_state = update_state
        self.game_over = False

        pygame.display.set_caption("Garbage Car Driver")

        self.border_width, self.border_height = surface.get_size()
        self.border = pygame.Rect(0, 80, self.border_width, self.border_height)
        super().__init__(surface)

