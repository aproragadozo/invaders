import pygame
from laser import Laser

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.image.load("graphics/spaceship.png")
        self.rect = self.image.get_rect(midbottom= (screen_width/2, screen_height-20))
        self.speed = 6
        self.lasers = pygame.sprite.Group()

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            if self.rect.x <= self.screen_width - self.rect.width:
                self.rect.x += self.speed
        if keys[pygame.K_LEFT]:
            if self.rect.x >= 0:
                self.rect.x -= self.speed
        if keys[pygame.K_SPACE]:
            if len(self.lasers) == 0:
                laser = Laser(self.rect.center, self.speed, self.screen_height)
                self.lasers.add(laser)
    
    def update(self):
        self.get_input()
        self.lasers.update()