import pygame
from typing import List, Tuple

class AnimatedAlien(pygame.sprite.Sprite):
    def __init__(self, pos: Tuple[int, int], sprite_paths: List[str]):
        """
        Initialize animated alien enemy
        
        Args:
            pos: Initial (x,y) position
            sprite_paths: List of paths to sprite images for animation states
        """
        super().__init__()
        
        # Load sprite states
        self.sprites = []
        for path in sprite_paths:
            sprite = pygame.image.load(path).convert_alpha()
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
        
        # Check screen boundaries
        if self.rect.right >= 800 or self.rect.left <= 0:
            self.direction *= -1  # Reverse direction
            self.rect.y += self.drop_distance  # Move down
            
        # Update animation
        self.animate(pygame.time.get_ticks())