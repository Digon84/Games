
class Game:
    def __init__(self, surface):
        self.surface = surface
        self.start_game()

    def start_game(self):
        raise NotImplementedError()

    def init_game(self):
        raise NotImplementedError()

    def restart_game(self):
        raise NotImplementedError()

    def draw_window(self):
        raise NotImplementedError()

    def play_game(self):
        raise NotImplementedError()


