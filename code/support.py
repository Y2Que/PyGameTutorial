
import pygame
from pathlib import Path
from csv import reader

def import_csv_layout(path):
    
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

def import_folder(strPath):
    surface_list = []

    myPath = Path.cwd() / strPath
    for image_path in myPath.iterdir():
        image_surf = pygame.image.load(image_path).convert_alpha()
        surface_list.append(image_surf)
    
    return surface_list
