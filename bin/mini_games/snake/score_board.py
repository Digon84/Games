import pygame


class ScoreBoard:
    def __init__(self, surface):
        super().__init__()
        self.display_surface = surface
        self.score = 0
        self.score_font = pygame.font.Font('../assets/score_board/fonts/score_board.TTF', size=40)
        self.game_over_font = pygame.font.Font('../assets/score_board/fonts/score_board.TTF', size=50)
        self.write_score()

    def increase_score(self):
        self.score += 1

    def write_score(self):
        score_amount_surface = self.score_font.render(str(self.score), False, "Black")
        display_x, _ = [value / 2 for value in self.display_surface.get_size()]
        score_amount_rect = score_amount_surface.get_rect(center=(display_x, 40))
        self.display_surface.blit(score_amount_surface, score_amount_rect)

    def update_score(self):
        self.increase_score()
        self.write_score()

    def game_over(self):
        game_over_surface = self.game_over_font.render("KONIEC", False, "Red")
        display_x, display_y = [value / 2 for value in self.display_surface.get_size()]
        game_over_rect = game_over_surface.get_rect(center=(display_x, display_y))
        self.display_surface.blit(game_over_surface, game_over_rect)
