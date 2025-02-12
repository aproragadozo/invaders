import pygame
pygame.init()
screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption('Drawing')

alien = pygame.image.load('graphics/aliensprite.png').convert_alpha()

sprite_one = alien.subsurface((25, 132, 90, 70))
sprite_two = alien.subsurface((130, 132, 90, 70))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill((60, 0, 100))
    screen.blit(sprite_one, (50, 50))
    screen.blit(sprite_two, (150, 50))
    pygame.display.update()

pygame.quit()