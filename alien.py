import pygame
from typing import List, Tuple


class SpriteSheet:
    def __init__(self, sheet_path):
        self.sheet = pygame.image.load(sheet_path).convert_alpha()
        
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        return sprite

class AnimatedAlien(pygame.sprite.Sprite):
    def __init__(self, pos: Tuple[int, int], spritesheet, 
                 frame_coords: List[Tuple[int, int]], sprite_size: Tuple[int, int]):
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
        
    def animate(self, current_time: int) -> None:
        if current_time - self.animation_timer > self.ANIMATION_DELAY:
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
            self.image = self.sprites[self.current_sprite]
            self.animation_timer = current_time
            
    def update(self) -> None:
        self.animate(pygame.time.get_ticks())

class AlienFleet(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.speed = 1
        self.direction = 1
        self.drop_distance = 40
    
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