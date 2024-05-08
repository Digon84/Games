import pygame
import sys
import settings

from menu import Menu


class Game:
    def __init__(self):
        self.game = None
        self.surface = screen
        self.state = 'menu'
        self.menu = Menu(self.surface, settings.games,
                         self.update_state, self.start_game)

    def run(self, events):
        if self.state == 'menu':
            self.menu.run(events)
        else:
            print(f"GAME MODE: {self.state}")
            self.game.play_game()

    def handle_events(self, events):
        if self.state == 'menu':
            self.menu.handle_events(events)

    def update_state(self, game_choice):
        self.state = game_choice

    def start_game(self, game_class):
        self.game = game_class(self.surface, None)
        self.game.start_game()


pygame.init()
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("Simple games")
game = Game()

while True:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('white')

    game.run(events)
    pygame.display.update()
    clock.tick(60)
