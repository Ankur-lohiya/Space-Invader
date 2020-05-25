import pygame
import random
import math
from pygame import mixer

# intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 700))

# background
background = pygame.image.load('background.jpg')
mixer.music.load('background_sound.wav')
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
game_over = False

score = 0
font = pygame.font.Font('freesansbold.ttf', 20)
over_font = pygame.font.Font('freesansbold.ttf', 64)
textX = 10
textY = 10


def game_over_text():
    global game_over
    game_over = True
    score_value = over_font.render('Game Over', True, (0, 255, 0))
    screen.blit(score_value, (225, 350))


def show_score(x, y):
    score_value = font.render('Score :' + str(score), True, (0, 255, 0))
    screen.blit(score_value, (x, y))


# player
playerImg = pygame.image.load('rocket_game.png')
playerX = 370
playerY = 580
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
no_of_enemies=9
for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load('enemy_game.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 200))
    enemyY_change = 1.5

# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 580
bulletX_change = 0
bulletY_change = 20
bullet_state = "ready"


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(((enemyX - bulletX) ** 2) + ((enemyY - bulletY) ** 2))
    return distance


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(enemyImg,x, y):
    screen.blit(enemyImg, (x, y))


# game loop
running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_RIGHT and not game_over:
                playerX_change = 5
            if event.key == pygame.K_LEFT and not game_over:
                playerX_change = -5
            if event.key == pygame.K_SPACE and not game_over:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('bullet_sound.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, playerY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736
    for i in range(no_of_enemies):
        enemyY[i] += enemyY_change
        if enemyY[i] > 660 or isCollision(enemyX[i], enemyY[i], playerX, playerY) < 45:
            enemyY_change = 0
            game_over_text()
        enemy(enemyImg[i],enemyX[i], enemyY[i])
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision < 27:
            collision_Sound = mixer.Sound('explosion.wav')
            collision_Sound.play()
            bulletY = 580
            bullet_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(0, 400)
    if bulletY <= 0:
        bulletY = 580
        bullet_state = "ready"
    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
