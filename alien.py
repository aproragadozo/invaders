import pygame
import random
from typing import List, Tuple
from laser import Laser


class SpriteSheet:
    def __init__(self, sheet_path):
        self.sheet = pygame.image.load(sheet_path).convert_alpha()
        
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        return sprite

class AnimatedAlien(pygame.sprite.Sprite):
    def __init__(self, pos: Tuple[int, int], spritesheet, 
                 frame_coords: List[Tuple[int, int]], sprite_size: Tuple[int, int], points: int, color_tint=None):
        super().__init__()
        
        # Extract sprites from spritesheet
        self.sprites = []
        for x, y in frame_coords:
            sprite = spritesheet.get_sprite(x, y, sprite_size[0], sprite_size[1])
            # Scale if needed
            if sprite_size != (32, 32):
                sprite = pygame.transform.scale(sprite, (32, 32))
            self.sprites.append(sprite)
            
        # Animation properties
        self.current_sprite = 0
        self.animation_timer = 0
        self.ANIMATION_DELAY = 500  # Time between state changes in ms
        
        # Set up initial sprite state
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        # Give them lasers
        self.lasers = pygame.sprite.Group()

        # how many points is this alien worth
        self.points = points

        # color all the sprites
        if color_tint:
            for i in range(len(self.sprites)):
                sprite_copy = self.sprites[i].copy()
                """ Apply a color tint to the sprite. """
                tint_surface = pygame.Surface(sprite_copy.get_size(), pygame.SRCALPHA)
                tint_surface.fill(color_tint)
                sprite_copy.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_MULT)
                # replace the original sprite with the tinted one
                self.sprites[i] = sprite_copy

    def animate(self, current_time: int):
        if current_time - self.animation_timer > self.ANIMATION_DELAY:
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
            self.image = self.sprites[self.current_sprite]
            self.animation_timer = current_time

    def shoot_at_random(self):
        laser = Laser(self.rect.midbottom, -5, 600, alien_firing=True)
        self.lasers.add(laser)
            
    def update(self):
        self.animate(pygame.time.get_ticks())
        if random.random() < 0.001:
            self.shoot_at_random()
        self.lasers.update()

class AlienFleet(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.speed = 1
        self.direction = 1
        self.drop_distance = 40

    def find_aliens_near_player_shots(self, shot_positions, tolerance=50):
        potential_shooters = []
        
        for alien in self.sprites():
            for shot_x in shot_positions:
                # If alien is within tolerance distance of a player shot
                if abs(alien.rect.centerx - shot_x) < tolerance:
                    potential_shooters.append(alien)
                    break
        
        return potential_shooters
    
    def update(self):
        if not self.sprites():  # If no aliens left
            return
            
        # Find fleet boundaries
        leftmost = min(alien.rect.left for alien in self.sprites())
        rightmost = max(alien.rect.right for alien in self.sprites())
        
        # Check if any edge of fleet hits screen boundary
        if rightmost >= 800 or leftmost <= 0:
            self.direction *= -1
            # Move entire fleet down
            for alien in self.sprites():
                alien.rect.y += self.drop_distance
        
        # Move all aliens horizontally
        for alien in self.sprites():
            alien.rect.x += self.speed * self.direction
            alien.update()