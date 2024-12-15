import pygame


class Menu:
    def __init__(self, surface, games, update_state, start_game):
        self.display_surface = surface
        self.games = games
        self.selected = 0
        self.update_state = update_state
        self.start_game = start_game
        print(pygame.font.get_fonts())
        self.font = pygame.font.SysFont('Arial', size=50)

    def draw_menu(self):
        self.draw_items()
        self.draw_images()

    def draw_items(self):
        for i, item in enumerate(self.games):
            if i == self.selected:
                item_surface = self.font.render(str(item['name']['pl']), False, 'grey')
            else:
                item_surface = self.font.render(str(item['name']['pl']), False, 'black')
            item_position = item_surface.get_rect(midleft=(20, 50 + 70*i))
            self.display_surface.blit(item_surface, item_position)

    def draw_images(self):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                print("Key down")
                if event.key == pygame.K_UP:
                    print(f'selected: {self.selected}')
                    if self.selected > 0:
                        self.selected -= 1
                if event.key == pygame.K_DOWN:
                    print(f'selected: {self.selected}')
                    if self.selected < len(self.games) - 1:
                        self.selected += 1
                if event.key == pygame.K_RETURN:
                    self.update_state(self.games[self.selected])
                    self.start_game(self.games[self.selected]['class'])

    def run(self, events):
        self.handle_events(events)
        self.draw_menu()

