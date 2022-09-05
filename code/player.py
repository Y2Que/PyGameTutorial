
import pygame
from settings import *
from debug import debug
from pathlib import Path
from support import import_folder

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack):

        super().__init__(groups)
        self.image = pygame.image.load(Path.cwd() / 'graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-6, -20)

        # graphics setup
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

        # movement
        self.direction = pygame.math.Vector2()
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None 
        # get list of all potential sprite the palyer can collide with
        self.obstacle_sprites = obstacle_sprites

        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_swtich_time = None
        self.switch_duration_cooldown = 200

        # stats
        self.stats = {
            'health' : 100,
            'energy' : 60,
            'attack' : 10,
             'magic' : 4,
             'speed' : 6
        }
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.speed  = self.stats['speed']
        self.exp = 123


    def import_player_assets(self):

        self.animations = {
                      'up' : [],
                    'down' : [],
                    'left' : [],
                   'right' : [],
                 'up_idle' : [],
               'down_idle' : [],
               'left_idle' : [],
              'right_idle' : [],
               'up_attack' : [],
             'down_attack' : [],
             'left_attack' : [],
            'right_attack' : []
        }

        for animation in self.animations.keys():
            animation_path = Path('graphics/player/') / animation
            self.animations[animation] = import_folder(animation_path)

    def input(self):

        # ignore imput while attacking
        if not self. attacking:

            # get keys currently pressed
            keys = pygame.key.get_pressed()

            # movement input
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]: 
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT]: 
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            # attack input
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            # magic input
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
            
            # switch weapons
            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_swtich_time = pygame.time.get_ticks()
                if self.weapon_index < len(weapon_data) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                self.weapon = list(weapon_data.keys())[self.weapon_index]


    def get_status(self):
        
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'

        elif not self.attacking:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '_idle')

    def move(self, speed):

        # don't move player faster on diagonals
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # move player and check for collisions
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):

        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:           # loop thru all sprites
                if sprite.hitbox.colliderect(self.hitbox):     # if player overlaps with sprite
                    if self.direction.x > 0:               # player moving right
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:             # player moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:           # loop thru all sprites
                if sprite.hitbox.colliderect(self.hitbox):     # if player overlaps with sprite
                    if self.direction.y > 0:               # player moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:             # player moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_swtich_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

    def animate(self):
        animation = self.animations[self.status]
        
        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        # if anmiations have different dimension, recenter image
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.input()          # get user input
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed) # move player sprite