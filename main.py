import pygame, random, math, sys, time
import threading
from pygame import mixer

# initialize
pygame.mixer.init()
pygame.init()

# create screen
windowSize = (800, 600)
screen = pygame.display.set_mode(windowSize)

# title and icon
pygame.display.set_caption("Space Invaders!")
icon = pygame.image.load("ufo.png").convert_alpha()
pygame.display.set_icon(icon)

# background
background = pygame.image.load("background.jpg").convert_alpha()
background = pygame.transform.scale(background, (800, 600))

# sounds
laser = pygame.mixer.Sound("pewpew_2.wav")
boom = pygame.mixer.Sound("boom2.wav")

# clock
clock = pygame.time.Clock()

# game over screen
font = pygame.font.SysFont("arial", 64)
def game_over_text():
     label = font.render("GAME OVER", True, (255, 255, 255))
     screen.blit(label, (200, 250))

# player
playerImg = pygame.image.load("spaceship.png").convert_alpha()
playerImg = pygame.transform.scale(playerImg, (64, 64))
playerX = 370
playerY = 520
playerX_change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))

# bullet
bullet = pygame.image.load("bullet.png").convert_alpha()
bullet = pygame.transform.scale(bullet, (20, 20))
bullet = pygame.transform.rotate(bullet, 90)
bulletX = 0
bulletY = playerY - 30
bulletY_change = 5
bullet_state = "ready"

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemyNumber = 6
for i in range(enemyNumber):
     
    enemyImg.append(pygame.image.load("enemy.png").convert_alpha())
    # enemyImg = pygame.transform.scale(enemyImg, (64, 64))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

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


    # being able to quit the game

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             sys.exit()

        if event.type == pygame.KEYUP:
            playerX_change = 0

# spaceship movement, bullet firing

    is_key_pressed = pygame.key.get_pressed()

    if is_key_pressed[pygame.K_LEFT]:
        playerX_change -= 0.5
    if is_key_pressed[pygame.K_RIGHT]:
        playerX_change += 0.5
    if is_key_pressed[pygame.K_SPACE]:
        if bullet_state == "ready":
                        laser.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
                    
        
    playerX += playerX_change

    # horizontal boundaries
    if playerX<=0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # collision detection

    """ if abs(enemyX - bulletX) < 20 and abs(enemyY - bulletY) < 20:
         print("Hit!") """
    def isCollision(enemyX, enemyY, bulletX, bulletY):
         distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY, 2)))
         if distance < 27:
              return True
         else:
              return False

    # enemy moving down when they hit the wall
    for i in range(enemyNumber):
        enemyX[i] += enemyX_change[i]

        if enemyX[i]<=0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
             boom.play()
             bulletY = playerY - 30
             bullet_state = "ready"
             enemyX[i] = random.randint(0, 735)
             enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

        # game over
        game_over = isCollision(enemyX[i], enemyY[i], playerX, playerY)
        if game_over:
             boom.play()
             game_over_text()

    # bullet movement
    if bulletY <= 0:
        bulletY = playerY - 30
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    

    player(playerX, playerY)
    
    
    clock.tick(60)

    pygame.display.update()