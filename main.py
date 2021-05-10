import pygame
pygame.init()

screen = pygame.display.set_mode((800,600))
#background
background = pygame.image.load('./Image/background.png')
# title and icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('./Image/spaceship.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('./Image/player.png')
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImg = pygame.image.load('./Image/enemy.png')
enemyX = 400
enemyY = 480
enemyX_change = 0

# BULLET
bulletImg = pygame.image.load('./Image/bullet.png')
bulletX = 400
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y):
    screen.blit(enemyImg,(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y+10))
running = True
while running:
    screen.fill((0,0,0))
    #background Image
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 2.5
            if event.key == pygame.K_SPACE:
                fire_bullet(playerX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    #Bullet movement
    if bullet_state in "fire":
        fire_bullet(playerX,bulletY)
        bulletY -= bulletY_change
    player(playerX,playerY)
    enemy(enemyX,enemyY)
    pygame.display.update()