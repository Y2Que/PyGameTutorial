
import pygame
from pathlib import Path
from random import choice

from debug import debug
from settings import *
from support import *
from tile import Tile
from player import Player
from weapon import Weapon
from ui import UI

class Level:

    def __init__(self):

        # get display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None

        # create map sprites
        self.create_map()

        # user interface
        self.ui = UI()

    def create_map(self):

        layouts = {
            'boundary': import_csv_layout(Path.cwd() / 
                                          'map/map_FloorBlocks.csv'),
               'grass': import_csv_layout(Path.cwd() / 
                                          'map/map_Grass.csv'),
              'object': import_csv_layout(Path.cwd() / 
                                          'map/map_Objects.csv'),
        }

        graphics = {
              'grass' : import_folder('graphics/Grass'),
            'objects' : import_folder('graphics/Objects')
        }
         
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1': # ignore empty tiles
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        match style:
                            case 'boundary':
                                Tile((x, y), 
                                    [self.obstacle_sprites], 
                                    'invisible')
                            case 'grass':
                                random_grass_img = choice(graphics['grass'])
                                Tile((x,y),
                                     [self.visible_sprites, self.obstacle_sprites],
                                     'grass',
                                     random_grass_img)
                            case 'object':
                                # object file names are numbers
                                object_img =  graphics['objects'][int(col)]                               
                                
                                Tile((x,y),
                                     [self.visible_sprites, self.obstacle_sprites],
                                     'object',
                                     object_img)

                            case _:
                                pass

        
        self.player = Player((2000, 1400), 
                             [self.visible_sprites], 
                              self.obstacle_sprites,
                              self.create_attack,
                              self.destroy_attack)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
            self.current_attack = None

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)

class YSortCameraGroup(pygame.sprite.Group):

    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating floor
        self.floor_surf = pygame.image.load(Path.cwd() / 
                                            'graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))

    def custom_draw(self, player):

        # get offset
        self.offset.x = self.half_width - player.rect.centerx
        self.offset.y = self.half_height - player.rect.centery

        # drawing the floor
        floor_offset_pos = self.offset - self.floor_rect.topleft
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), 
                             key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_pos)