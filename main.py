import pygame, random, math

# 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 Access Token

# initializing pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))

running = True

# Background
background = pygame.image.load('background.png')


pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# player

playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(0, 768))
    enemyY.append(random.randint(25, 100))
    enemyX_change.append(2)
    enemyY_change.append(30)


# bullet 
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
bulletX_change = 0

bullet_state = 'ready'

# score system
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 20 )
textX = 10
textY = 10

def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY, 2)))
    if distance < 27:
        return True
    
    return False


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


over_font = pygame.font.Font('freesansbold.ttf', 34)


def game_over_text():
    over_text = over_font.render('Game Over', True, (255, 255, 255))
    screen.blit(over_text, (200, 200))


while running:

    screen.fill((0,0,0))
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    playerX += playerX_change
    
    if playerX < 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 450:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        
        if enemyX[i] < 0:
            enemyX_change[i] += 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 768:
            enemyX_change[i] += -2
            enemyY[i] += enemyY_change[i]
        
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 768)
            enemyY[i] = random.randint(25, 100)

        enemy(enemyX[i], enemyY[i], i)

        
    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()