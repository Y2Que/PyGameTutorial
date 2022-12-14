
import pygame

from settings import *

class UI:

    def __init__(self):
        
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT,
                                     UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10,
                                           10,
                                           HEALTH_BAR_WIDTH,
                                           BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10,
                                           34,
                                           ENERGY_BAR_WIDTH,
                                           BAR_HEIGHT)

    def show_bar(self, current_amount, max_amount, bg_rect, color):
        
        # draw bar background
        pygame.draw.rect(self.display_surface,
                         UI_BG_COLOR,
                         bg_rect)

        # convert stat to pixels
        ratio = current_amount / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # draw bar
        pygame.draw.rect(self.display_surface,
                         color,
                         current_rect)

        # draw bar
        pygame.draw.rect(self.display_surface,
                         UI_BORDER_COLOR,
                         bg_rect,
                         3)

    def show_exp(self):
        pass

    def display(self, player):
        self.show_bar(player.health,
                      player.stats['health'],
                      self.health_bar_rect,
                      HEALTH_COLOR)
        self.show_bar(player.energy,
                      player.stats['energy'],
                      self.energy_bar_rect,
                      ENERGY_COLOR)