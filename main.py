import pygame, random, math, sys, time
from pygame.sprite import Group, GroupSingle, spritecollide
from spaceship import Spaceship
from alien import AnimatedAlien, AlienFleet, SpriteSheet
import threading
from pygame import mixer

# initialize
pygame.mixer.init()
pygame.init()
# this is so that I can add a game over screen without quitting the game loop
game_on = True

# create screen
windowSize = (800, 600)
screen = pygame.display.set_mode(windowSize)

# title and icon
pygame.display.set_caption("Space Invaders!")
icon = pygame.image.load("graphics/ufo.png").convert_alpha()
pygame.display.set_icon(icon)

# make mouse invisible
pygame.mouse.set_visible(False)

# background
# background = pygame.image.load("graphics/background.jpg").convert_alpha()
# background = pygame.transform.scale(background, (800, 600))

# spritesheet with the aliens
spritesheet = SpriteSheet('graphics/aliensprite.png')
full_spritesheet = SpriteSheet('graphics/sprite-sheet.jpg')

# set up player
player_group = pygame.sprite.GroupSingle()

# add respawn delay when player dies
def respawn_player():
    time.sleep(1)
    if player_group.sprite:
        player_group.sprite.rect.center = (windowSize[0]/2, windowSize[1] - 50)

# sounds
laser = pygame.mixer.Sound("pewpew_2.wav")
boom = pygame.mixer.Sound("boom2.wav")

# clock
clock = pygame.time.Clock()

# track player shot x-coords
recent_player_shots = []
SHOT_MEMORY = 3

# alien color options
row_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

# game over screen
font = pygame.font.SysFont("arial", 64)
def game_over_text():
     label = font.render("GAME OVER", True, (255, 255, 255))
     screen.blit(label, (200, 250))

# victory screen
def victory_text():
    victory_label = font.render("VICTORY!", True, (255, 255, 0))  # Yellow text
    screen.blit(victory_label, (270, 250))
    
    restart_font = pygame.font.SysFont("arial", 32)
    restart_text = restart_font.render("Press R to play again", True, (255, 255, 255))
    screen.blit(restart_text, (250, 350))

def set_up_player():
    global player_group
    player_group.empty()
    # spaceship = Player(370, 520, "graphics/spaceship.png")
    player = Spaceship(windowSize[0], windowSize[1])
    player_group.add(player)

    #player score
    score_font = pygame.font.SysFont("arial", 15)
    score_display = score_font.render(f"Score: {player.score}", True, (255, 255, 0))
    screen.blit(score_display, (700, 10))

    if not player_group.sprite:
        print("ERROR: Player was not added to player_group!")

set_up_player()

invader_fleet = AlienFleet()
for row in range(3):
     points = 40 - (row + 1) * 10
     for col in range(8):
          pos = (col * 50 + 50, row * 50 + 40)
          alien_color = row_colors[row]
          invader = AnimatedAlien(pos, spritesheet, [(25, 132), (130, 132)], (90, 70), points, alien_color)
          invader_fleet.add(invader)

respawn_timer = 0

victory = False

# game loop
running = True
while running:
    screen.fill((188, 127, 205))

    # background image
    # screen.blit(background, (0, 0))
    screen.fill ((0, 0, 0))


    # being able to quit the game

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             pygame.quit()
             sys.exit()

    # display player lives
    for i in range(player_group.sprite.lives):
        life = pygame.image.load("graphics/spaceship.png").convert_alpha()
        life = pygame.transform.scale(life, (20, 20))
        screen.blit(life, (10 + i * 30, 10))

    if victory:
        victory_text()
    
    # same restart logic as for game over - should be reused instead of copied
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reset game state
            game_on = True
            victory = False
            # Reset player
            set_up_player()
            # Recreate alien fleet
            invader_fleet.empty()
            for row in range(3):
                # set point score based on position
                points = 40 - (row + 1) * 10
                for col in range(8):
                    pos = (col * 50 + 50, row * 50 + 40)
                    invader = AnimatedAlien(pos, spritesheet, [(25, 132), (130, 132)], (90, 70), points)
                    invader_fleet.add(invader)

    # game over screen and restart logic
    elif not game_on:
        game_over_text()
        restart_font = pygame.font.SysFont("arial", 32)
        restart_text = restart_font.render("Press R to restart", True, (255, 255, 255))
        screen.blit(restart_text, (250, 350))
        
        # Check for restart input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reset game state
            game_on = True
            # Reset player
            set_up_player()
            # Recreate alien fleet
            invader_fleet.empty()
            for row in range(3):
                points = 40 - (row + 1) * 10
                for col in range(8):
                    pos = (col * 50 + 50, row * 50 + 40)
                    invader = AnimatedAlien(pos, spritesheet, [(25, 132), (130, 132)], (90, 70), points)
                    invader_fleet.add(invader)
            respawn_timer = 0

    # drawing (but only if the player is still alive)
    if game_on:
        # print("DEBUG: player_group.sprite exists?", player_group.sprite is not None)
        player_group.update()
        # aliens targeted shooting
        if recent_player_shots and random.random() < 0.05:
            shooters = invader_fleet.find_aliens_near_player_shots(recent_player_shots)
            if shooters:
                # Select one to shhot
                shooter = random.choice(shooters)
                shooter.shoot_at_random() 

        invader_fleet.update()

        # display score
        if player_group.sprite:
            score_font = pygame.font.SysFont("arial", 15)
            score_display = score_font.render(f"Score: {player_group.sprite.score}", True, (255, 255, 0))
            screen.blit(score_display, (650, 20))

        # victory screen
        if len(invader_fleet) == 0:
            victory = True
            game_on = False

    # Add collision detection
        if player_group.sprite and hasattr(player_group.sprite, 'lasers'):
            for laser in player_group.sprite.lasers:
                # add the x position of the laser to the list of recent player shots
                if laser.x_position not in recent_player_shots:
                    recent_player_shots.append(laser.x_position)
                    # keep only the last 3
                    if len(recent_player_shots) > SHOT_MEMORY:
                        recent_player_shots.pop(0)
                aliens_hit = pygame.sprite.spritecollide(laser, invader_fleet, True)
                if aliens_hit:
                    # add the destroyed alien's points to the player's score
                    for alien in aliens_hit:
                        player_group.sprite.increment_score(alien.points)
                    laser.kill()
                    boom.play()

            player_group.sprite.lasers.draw(screen)

            for alien in invader_fleet:
                for laser in alien.lasers:
                    if pygame.sprite.spritecollide(laser, player_group, False):
                        laser.kill() # destroy the destroying laser
                        boom.play()
                        player_group.sprite.lose_life()
                        if player_group.sprite.lives == 0:
                            # if the player dies
                            game_on = False # game over
                        else:
                            respawn_timer = pygame.time.get_ticks() + 1000
                            # hide player while respawn
                            player_group.sprite.rect.center = (-100, -100)
                            
            # the collision detection doesn't remove the player!
            if player_group.sprite and pygame.sprite.spritecollide(player_group.sprite, invader_fleet, False):
                boom.play()
                player_group.sprite.lose_life()
                if player_group.sprite.lives == 0:
                    # if the player dies
                    game_on = False # game over
                else:
                    respawn_timer = pygame.time.get_ticks() + 1000
                    # hide player while respawn
                    player_group.sprite.rect.center = (-100, -100)
            
            if respawn_timer > 0 and pygame.time.get_ticks() > respawn_timer:
                if player_group.sprite:  
                    player_group.sprite.rect.center = (windowSize[0] // 2, windowSize[1] - 50)
                respawn_timer = 0  # Reset timer

            player_group.draw(screen)
            
        invader_fleet.draw(screen)
    # make the alien shots show up
        for alien in invader_fleet:
            alien.lasers.draw(screen)
    
    clock.tick(60)

    pygame.display.update()