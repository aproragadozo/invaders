import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, position, speed, screen_height, alien_firing = False):
        super().__init__()
        self.image = pygame.Surface((4,15))
        self.image.fill((243, 216, 63))
        self.rect = self.image.get_rect(center = position)
        self.speed = speed if not alien_firing else -speed
        self.screen_height = screen_height
        self.fire = True

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > self.screen_height:
            self.fire = False
            self.kill()