import pygame
import random

# initialize
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# title and icon
pygame.display.set_caption("Space Invaders!")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load("spaceship.png")
playerImg = pygame.transform.scale(playerImg, (64, 64))
playerX = 370
playerY = 520
playerX_change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))

# enemy
enemyImg = pygame.image.load("enemy.png")
# enemyImg = pygame.transform.scale(enemyImg, (64, 64))
enemyX = random.randint(0, 800)
enemyY = random.randint(50, 150)
enemyX_change = 0.08
enemyY_change = 40

def enemy(x, y):
    screen.blit(enemyImg, (x, y))

# game loop
running = True
while running:

    screen.fill((188, 127, 205))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_LEFT:
                    playerX_change -= 0.2
                case pygame.K_RIGHT:
                    playerX_change += 0.2
        if event.type == pygame.KEYUP:
            playerX_change = 0

   
    playerX += playerX_change
    # horizontal boundaries
    if playerX<=0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy moving down when they hit the wall
    enemyX += enemyX_change

    if enemyX<=0:
        enemyX_change = 0.08
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -0.08
        enemyY += enemyY_change
    
    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()