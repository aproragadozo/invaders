import pygame

# initialize
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# title and icon
pygame.display.set_caption("Space Invaders!")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)


# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((188, 127, 205))
    pygame.display.update()