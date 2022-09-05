import pygame, sys
from settings import *
from debug import debug
from level import Level

class Game:

    def __init__(self):

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Zelda Tribute')
        
        self.level = Level()

    def run(self):
        while True: # main game loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

# check if main.py is run directly, not called
if __name__ == '__main__':
    game = Game()
    game.run()