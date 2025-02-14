import pygame
pygame.init()
screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption('Drawing')

spritesheet = pygame.image.load('graphics/sprite-sheet.jpg').convert_alpha()

sprite_one = spritesheet.subsurface((25, 132, 90, 70))
sprite_two = spritesheet.subsurface((130, 132, 90, 70))
bullet = spritesheet.subsurface((475, 890, 25, 50))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill((60, 0, 100))
    # screen.blit(sprite_one, (0, 0))
    # screen.blit(sprite_two, (100, 0))
    screen.blit(bullet, (150, 0))
    pygame.display.update()

pygame.quit()