import pygame
import math
import random
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800,600))
#background
background = pygame.image.load('./Image/background.png')
#background sound
mixer.music.load('./music/background.wav')
mixer.music.play(-1)

# title and icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('./Image/spaceship.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('./Image/player.png')
playerX = 370
playerY = 480
playerX_change = 0
health = 1
# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('./Image/enemy.png'))
    enemyX.append(random.randint(0,500))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(0.25)
# BULLET
bulletImg = pygame.image.load('./Image/bullet.png')
bulletX = 400
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

#Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

#Game over
over_font = pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    score = font.render("Score: " + str(score_value),True, (255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))
def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y+10))
    

def isCollision(aX,aY,bX,bY):
    dist = math.sqrt(math.pow(aX-bX,2) + math.pow(aY-bY,2) )
    if dist < 27:
        return True
    else:
        return False
running = True
while running:
    num_invader = 0
    screen.fill((0,0,0))
    #background Image
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if health != 0:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -3.5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 3.5
                if event.key == pygame.K_SPACE:
                    if bullet_state is "ready":
                        bullet_Sound = mixer.Sound('./music/laser.wav')
                        bullet_Sound.play()
                        bulletX = playerX
                        fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
# enemy movement 
    
    for i in range(num_of_enemies):
        if isCollision(enemyX[i],enemyY[i],playerX,playerY):
            health -= 1
        if enemyY[i] > 500:
            num_invader += 1
        if score_value >= 100:
            enemyY_change[i] = 0.3575
        enemyY[i] += enemyY_change[i]
        # collision 
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_Sound = mixer.Sound('./music/explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 10
            enemyX[i] = random.randint(0,700)
            enemyY[i] = random.randint(50,150)
        enemy(enemyX[i],enemyY[i],i)

    #Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state in "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change
    if health == 0:
        for i in range(num_of_enemies):
            enemyX[i] = 2000
        game_over_text()
    if num_invader >= 5:
        game_over_text()
        health = 0

    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()