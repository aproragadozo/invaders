import pygame
from typing import List, Tuple

class AnimatedAlien(pygame.sprite.Sprite):
    def __init__(self, pos: Tuple[int, int], spritesheet, 
                 frame_coords: List[Tuple[int, int]], sprite_size: Tuple[int, int]):
        """
        Initialize animated alien enemy using spritesheet
        
        Args:
            pos: Initial (x,y) position
            spritesheet: SpriteSheet object containing all sprites
            frame_coords: List of (x,y) coordinates for each animation frame in the spritesheet
            sprite_size: (width, height) of each sprite frame
        """
        super().__init__()
        
        # Extract sprites from spritesheet
        self.sprites = []
        for x, y in frame_coords:
            sprite = spritesheet.subsurface(x, y, sprite_size[0], sprite_size[1])
            # Scale if needed (64x64 is target size from original code)
            if sprite_size != (64, 64):
                sprite = pygame.transform.scale(sprite, (64, 64))
            self.sprites.append(sprite)
            
        # Animation properties
        self.current_sprite = 0
        self.animation_timer = 0
        self.ANIMATION_DELAY = 500  # Time between state changes in ms
        
        # Movement properties 
        self.speed = 2
        self.direction = 1
        self.drop_distance = 40
        
        # Set up initial sprite state
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
    def animate(self, current_time: int) -> None:
        """
        Update sprite animation state based on timer
        
        Args:
            current_time: Current game time in milliseconds
        """
        if current_time - self.animation_timer > self.ANIMATION_DELAY:
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
            self.image = self.sprites[self.current_sprite]
            self.animation_timer = current_time
            
    def update(self) -> None:
        """Update alien position and animation state"""
        # Move horizontally
        self.rect.x += self.speed * self.direction