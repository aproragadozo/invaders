import pygame
import random
import threading

# initialize
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# title and icon
pygame.display.set_caption("Space Invaders!")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# background
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (800, 600))

# player
playerImg = pygame.image.load("spaceship.png")
playerImg = pygame.transform.scale(playerImg, (64, 64))
playerX = 370
playerY = 520
playerX_change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))

# bullet
bullet = pygame.image.load("bullet.png")
bullet = pygame.transform.scale(bullet, (20, 20))
bullet = pygame.transform.rotate(bullet, 90)
bulletY = playerY - 30
bulletY_change = 1
bullet_state = "ready"

# enemy
enemyImg = pygame.image.load("enemy.png")
# enemyImg = pygame.transform.scale(enemyImg, (64, 64))
enemyX = random.randint(0, 800)
enemyY = random.randint(50, 150)
enemyX_change = 0.08
enemyY_change = 40

def enemy(x, y):
    screen.blit(enemyImg, (x, y))

# fire bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x+18, y+20))

# game loop
running = True
while running:

    screen.fill((188, 127, 205))

    # background image
    screen.blit(background, (0, 0))


    # spaceship movement, bullet firing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_LEFT:
                    playerX_change -= 0.2
                case pygame.K_RIGHT:
                    playerX_change += 0.2
                case pygame.K_SPACE:
                    if bullet_state is "ready":
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
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

    # bullet movement
    if bulletY <= 0:
        bulletY = playerY - 30
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()