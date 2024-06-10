import pygame, random, math, sys, time
from spaceship import Spaceship
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

# make mouse invisible
pygame.mouse.set_visible(False)

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
# should remove the x_change prop later
class Player(pygame.sprite.Sprite):
     def __init__(self, pos_x, pos_y, img_path):
          super().__init__()
          self.image = pygame.image.load(img_path).convert_alpha()
          self.image = pygame.transform.scale(self.image, (64, 64))
          self.rect = self.image.get_rect()
          self.rect.center = [pos_x, pos_y]
          self.moveX = 0
          
     def moveRight(self):
          self.moveX += 0.05

     def moveLeft(self):
          self.moveX -= 0.05

     def update(self):
         self.rect.x += self.moveX

spaceship = Player(370, 520, "spaceship.png")
player_group = pygame.sprite.GroupSingle()
player = Spaceship(windowSize[0], windowSize[1])
player_group.add(player)



# bullet

bullet = pygame.image.load("bullet.png").convert_alpha()
bullet = pygame.transform.scale(bullet, (20, 20))
bullet = pygame.transform.rotate(bullet, 90)
bulletX = 0
# bulletY = spaceship.top - 30
bulletY = spaceship.rect.y - 30
bulletY_change = 5
bullet_state = "ready"

# enemy
class Alien(pygame.sprite.Sprite):
    def __init__(self, img_path):
        super().__init__()
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

invader = Alien("enemy.png")
invader_fleet = pygame.sprite.Group()
invader_fleet.add(invader)

class Enemy:
     def __init__(self, image, x, y, speed, skip, direction):
        self.image = image
        self.x = x
        self.y = y
        self.speed = speed
        self.skip = skip
        self.direction = direction

     def collision(self, obstacleX, obstacleY):
        distance = math.sqrt((math.pow(self.x-obstacleX,2)) + (math.pow(self.y-obstacleY, 2)))
        if distance < 27:
              return True
        else:
              return False

invaders = []

""" enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = [] """
enemyNumber = 6
for i in range(enemyNumber):
     
     i = Enemy(pygame.image.load("enemy.png").convert_alpha(), random.randint(0, 735), random.randint(50, 150), 2, 40, 1)
     
     invaders.append(i)

     """ enemyImg.append(pygame.image.load("enemy.png").convert_alpha())
     # enemyImg = pygame.transform.scale(enemyImg, (64, 64))
     enemyX.append(random.randint(0, 735))
     enemyY.append(random.randint(50, 150))
     enemyX_change.append(2)
     enemyY_change.append(40) """

'''
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))
'''

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
             pygame.quit()
             sys.exit()

        if event.type == pygame.KEYUP:
            #spaceship.left_change = 0
            spaceship.moveX = 0

# spaceship movement, bullet firing

    is_key_pressed = pygame.key.get_pressed()

    if is_key_pressed[pygame.K_LEFT]:
        #spaceship.left_change -= 0.5
        #spaceship.x_change -= 0.5
        print(spaceship.rect.x)
        spaceship.moveLeft()
        print(spaceship.rect.x)
    if is_key_pressed[pygame.K_RIGHT]:
        # spaceship.left_change += 0.5
        #spaceship.x_change += 0.5
        spaceship.moveRight()
    if is_key_pressed[pygame.K_SPACE]:
        if bullet_state == "ready":
            laser.play()
            bulletX = spaceship.rect.x
            fire_bullet(bulletX, bulletY)
                    
        
    # spaceship.left += spaceship.left_change

    # horizontal boundaries
    if spaceship.rect.x<=0:
        spaceship.rect.x = 0
    elif spaceship.rect.x >= windowSize[0] - spaceship.rect.width:
        spaceship.rect.x = windowSize[0] - spaceship.rect.width

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
    for i in invaders:
        i.x += i.speed * i.direction

        if i.x <=0 or i.x >= windowSize[0] - i.image.get_size()[0]:
            # enemyX_change[i] = 2
            i.y += i.skip
            i.direction *= -1

        # collision
        collision = i.collision(bulletX, bulletY)
        if collision:
             boom.play()
             bulletY = spaceship.rect.y - 30
             bullet_state = "ready"
             i.x = random.randint(0, 735)
             i.y = random.randint(50, 150)

        # screen.blit(i.image, (i.x, i.y))

        # game over
        game_over = isCollision(i.x, i.y, spaceship.rect.x, spaceship.rect.y)
        if game_over:
             boom.play()
             game_over_text()

    # bullet movement
    if bulletY <= 0:
        bulletY = spaceship.rect.y - 30
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    

    # player(spaceship.left, spaceship.top)
    player_group.update()
    invader_fleet.update()
    player_group.draw(screen)
    player_group.sprite.lasers.draw(screen)
    invader_fleet.draw(screen)
    
    clock.tick(60)

    pygame.display.update()