import pygame
import math
import time
import random
import os
from pygame import mixer

#load image
PLAYER = pygame.image.load(os.path.join("Image","player.png"))
ENEMY = pygame.image.load(os.path.join("Image","enemy.png"))
UFO = pygame.image.load(os.path.join("Image","ufo.png"))
UFO1 = pygame.image.load(os.path.join("Image","ufo1.png"))
BULLET = pygame.image.load(os.path.join("Image","bullet.png"))
ALIEN = pygame.image.load(os.path.join("Image","alien.png"))
ALIEN1 = pygame.image.load(os.path.join("Image","alien1.png"))

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
#background
background = pygame.image.load('./Image/background.png')
#background sound
mixer.music.load('./music/background.wav')
mixer.music.play(-1)

# title and icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('./Image/spaceship.png')
pygame.display.set_icon(icon)

#Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

#Game over
over_font = pygame.font.Font('freesansbold.ttf',64)
def show_score(x,y):
    score = font.render("Score: " + str(score_value),True, (255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))

class Bullet:
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self,screen):
        screen.blit(self.img,(self.x,self.y))

    def  move(self,vel):
        self.y += vel

    def off_screen(self,height):
        return not (self.y <= height and self.y >= 0)

    def collision(self,obj):
        return collide(self,obj)

class Ship:
    COOLDOWN = 30
    def __init__(self,x,y,type,health = 100):
        self.x = x
        self.y = y
        self.type = type
        self.health = health
        self.ship_img = None
        self.bullet_img = None
        self.bullets = []
        self.cool_down_counter = 0 
    def draw(self,screen):
        screen.blit(self.ship_img,(self.x,self.y))
        for bullet in self.bullets:
            bullet.draw(screen)

    def move_bullet(self,vel,obj):
        self.cooldown()
        for bullet in self.bullets:
            bullet.move(vel)
            if bullet.off_screen(screen_height):
                self.bullets.remove(bullet)
            elif bullet.collision(obj):
                obj.health -= 10
                self.bullets.remove(bullet)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
    
    def shoot(self):
        if self.cool_down_counter == 0:
            bullet = Bullet(self.x+15,self.y-10,self.bullet_img)
            self.bullets.append(bullet)
            self.cool_down_counter = 1

class Player(Ship):
    def __init__(self,x,y,health = 100):
        super().__init__(x,y,health)
        self.ship_img = PLAYER
        self.bullet_img = BULLET
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
    
    def move_bullet(self,vel,objs):
        self.cooldown()
        for bullet in self.bullets:
            bullet.move(vel)
            if bullet.off_screen(screen_height):
                self.bullets.remove(bullet)

            else:
                for obj in objs:
                    if bullet.collision(obj):
                        objs.remove(obj)
                        self.bullets.remove(bullet)
                        explosion_Sound = mixer.Sound('./music/explosion.wav')
                        explosion_Sound.play()

                        

    def draw(self,screen):
        super().draw(screen)
        self.healthbar(screen)
    def healthbar(self,screen):
        pygame.draw.rect(screen,(255,0,0),(self.x,self.y+64+10,64,10))
        pygame.draw.rect(screen,(0,255,0),(self.x,self.y + 64 + 10,64*(self.health/self.max_health),10))

class Enemy(Ship):
    TYPE = {
        "enemy": (ENEMY,ALIEN),
        "ufo": (UFO,ALIEN),
        "ufo1": (UFO1,ALIEN1)
    }
    def __init__(self,x,y,type,health = 100):
        super().__init__(x,y,health)
        self.ship_img, self.bullet_img = self.TYPE[type]
        self.mask = pygame.mask.from_surface(self.ship_img)
        
    def move(self,changeY):
        self.y += changeY

def collide(obj1,obj2):
    dist = math.sqrt(math.pow(obj1.x-obj2.x,2) + math.pow(obj1.y-obj2.y,2))
    if dist < 27:
        return True
    else:
        return False

def main():
    FPS = 60
    level = 0
    main_font = pygame.font.SysFont("freesansbold.ttf",50)

    player =Player(375,500)
    clock = pygame.time.Clock()
    running = True
    lives = 5
    lost = False
    enemies = []
    num_of_enemy = 5
    enemyY_change = 1

    playerX_change = 5
    playerY_change = 5
    enemy_bulletY_change = 5
    bulletY_change = 10
    def redraw_window():
        screen.blit(background,(0,0))
        level_label = main_font.render(f"Level: {level}",1,(255,255,255))
        lives_label = main_font.render(f"Lives: {lives}",1,(255,255,255))
        screen.blit(level_label,(650,0))
        screen.blit(lives_label,(10,10))
        
        for enemy in enemies:
            enemy.draw(screen)
        #show_score(10,10)
        player.draw(screen)

        if lost:
            game_over_text()

        pygame.display.update()
    while running:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True

        if len(enemies) == 0:
            level += 1
            num_of_enemy += 5
            for i in range(num_of_enemy):
                enemy = Enemy(random.randrange(50,screen_width-100),random.randrange(-1500,-100),random.choice(["enemy","ufo","ufo1"]))
                enemies.append(enemy)
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if lost == False:
            keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= playerX_change

        if keys[pygame.K_RIGHT]:
            player.x += playerX_change

        if keys[pygame.K_UP]:
            player.y -= playerY_change

        if keys[pygame.K_DOWN]:
            player.y += playerY_change
        
        if keys[pygame.K_SPACE]:       
            laser_Sound = mixer.Sound('./music/laser.wav')
            laser_Sound.play()
            player.shoot()

        if player.x <= 0:
            player.x = 0
        elif player.x >= 736:
            player.x= 736 
        if player.y <= 0:
            player.y = 0
        elif player.y >=500:
            player.y= 500
        
        for enemy in enemies[:]:
            enemy.move(enemyY_change)
            enemy.move_bullet(bulletY_change,player)
            if random.randrange(0,2*60) == 1:
                enemy.shoot()
            if collide(enemy,player):
                player.health -= 10
                enemies.remove(enemy)
            if enemy.y > screen_height:
                lives -= 1
                enemies.remove(enemy)

        player.move_bullet(-bulletY_change,enemies)
 
def main_menu():
    title_font = pygame.font.SysFont("comicsans",70)
    run = True
    while run:
        screen.blit(background,(0,0))
        title_label = title_font.render("Press the mouse to begin",1,(255,255,255))
        screen.blit(title_label,(100,250))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()
main_menu()
