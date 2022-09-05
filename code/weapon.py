
import pygame
from pathlib import Path

class Weapon(pygame.sprite.Sprite):

    def __init__(self, player, groups):
        
        super().__init__(groups)
        direction = player.status.split('_')[0]

        # graphic
        full_path = Path.cwd() / f'graphics/weapons/{player.weapon}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        # placement
        match direction:
            case 'left':
                self.rect = self.image.get_rect(midright = player.rect.midleft +
                                                pygame.math.Vector2(0,16))
            case 'right':
                self.rect = self.image.get_rect(midleft = player.rect.midright +
                                                pygame.math.Vector2(0,16))
            case 'up':
                self.rect = self.image.get_rect(midbottom = player.rect.midtop +
                                                pygame.math.Vector2(-12,0))
            case 'down':
                self.rect = self.image.get_rect(midtop = player.rect.midbottom +
                                                pygame.math.Vector2(-12,0))
            case _:
                pass