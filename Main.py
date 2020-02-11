import pygame, random, math
from pygame import mixer
# Initialize the pygame
pygame.init()

# create the screen (width, height)
screen = pygame.display.set_mode((800,600))

# background
background = pygame.image.load("background.png")


# Title and Icon
pygame.display.set_caption("Escape from Algorift")
icon = pygame.image.load("rocket.png")
pygame.display.set_icon(icon)

# Music
pygame.mixer.music.load("sibg.mp3")
pygame.mixer.music.play(-1, 0.00)
pygame.mixer.music.set_volume(1)
print(pygame.mixer.music.get_volume())


# Player (x and y are size of 'Player')
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0
#playerY_change = 0

# Enemy
enemyImg = pygame.image.load("enemy.png")
enemyX = random.randint(0, 735)   #Changed from "(0, 800)" because enemy movement interfered if spawn was greater than
enemyY = random.randint(50, 150)  #736 because of the rules that were set for it
enemyX_change = 2
enemyY_change = 40

# Bullet
bulletImg = pygame.image.load("laserbeam.png")
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "ready"

# Score
score = 0

def isCollision (enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        if bullet_state == "fire":
            return True
    else:
        return False

def playerCollision (enemyX, enemyY, playerX, playerY):
    distance_p = math.sqrt((math.pow(enemyX-playerX,2)) + (math.pow(enemyY-playerY, 2)))
    if distance_p < 27:
        return True
    else:
        return False



def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def player(x, y):
    # blit is used to draw
    screen.blit(playerImg, (x, y))

# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue values
    screen.fill((50, 50, 100))
    # background image
    screen.blit(background, (0,0))

    # events are anything that is happening inside game window, like keyboard inputs or clicking
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # QUIT is a quit event, clicking the X on the window
            running = False

    # if key stroke is pressed, check whether it is right or left
        if event.type == pygame.KEYDOWN: # down is any key being pressed "down"
            if event.key == pygame.K_LEFT:
                playerX_change = -3.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 3.5
            #if event.key == pygame.K_UP:
              #  playerY_change = -2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP: # up is when key is released "up"
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
               playerX_change = 0
           # if event.key == pygame.K_UP:
             #   playerY_change = 0


    playerX += playerX_change
    #playerY += playerY_change

# setting window border for our Player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

# enemy border and movement
    enemyX += enemyX_change

    if enemyX <= 0:
        enemyX_change = 2.5
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -2.5
        enemyY += enemyY_change

# Bullet movement

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Putting the collision of the laser and the player to work
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        #enemyImg = pygame.image.load("explosion.png")
        enemy_sound = mixer.Sound("explosion.wav")
        enemy_sound.play()
        bulletY = 480
        bullet_state = "ready"
        score += 1
        print(score)
        enemyX = random.randint(0, 735)
        enemyY = random.randint(50, 150)


    # Putting the collision of the enemy and the player to work
    collision_p = playerCollision(enemyX, enemyY, playerX, playerY)
    if collision_p:
        print("Game over")

    player(playerX, playerY)
    enemy(enemyX, enemyY)
    # Need to make sure screen is constantly updated
    pygame.display.update()
