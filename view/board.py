import pygame


class Board:
    def __init__(
            self,
            win_width,
            win_height,
            border,
            bg_color,
            surf_color
    ):
        self.win_width = win_width
        self.win_height = win_height
        self.border = border
        self.bg_color = bg_color
        self.surf_color = surf_color

        self.window, self.surface = self.init_window()

    def init_window(self):
        pygame.display.set_caption("Hunter")

        window = pygame.display.set_mode((self.win_width, self.win_height))
        surface = pygame.Surface((self.win_width - self.border, self.win_height - self.border))

        return window, surface

    def update_window(self):
        self.window.fill(self.bg_color)
        self.surface.fill(self.surf_color)
        self.window.blit(self.surface, (self.border / 2, self.border / 2))

    def stop_game(self, text_message):
        self.window.fill(self.bg_color)

        new_surface = pygame.Surface((self.win_width - self.border * 4, self.win_height - self.border * 4))
        new_surface.fill((200, 200, 200))

        font = pygame.font.SysFont('liberationserif', 100)
        text = font.render(text_message, True, (0, 0, 250))
        new_surface = text.get_rect()
        new_surface.center = (self.win_width // 2, self.win_height // 2)
        self.window.blit(text, (self.border*2, self.border*2))
