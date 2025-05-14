import pygame
from pygame import *

# Initialize Pygame and setup display
pygame.init()
display.set_caption('Лабиринт')  # 'Labyrinth' in Russian
window = display.set_mode((600, 600))

# Definitions
win_width = 600
win_height = 600

# Load background image
try:
    background = transform.scale(image.load('as.jpg'), (win_width, win_height))
except pygame.error as e:
    print(f"Не удалось загрузить фоновое изображение: {e}")
    background = Surface((win_width, win_height))

# GameSprite class
class GameSprite(sprite.Sprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed=0, player_y_speed=0):
        super().__init__(player_image, size_x, size_y, player_x, player_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    
    def update(self, barriers):
        if 0 < self.rect.x + self.x_speed < win_width - self.rect.width:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        for p in platforms_touched:
            if self.x_speed > 0:
                self.rect.right = min(self.rect.right, p.rect.left)
            if self.x_speed < 0:
                self.rect.left = max(self.rect.left, p.rect.right)

        if 0 < self.rect.y + self.y_speed < win_height - self.rect.height:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        for p in platforms_touched:
            if self.y_speed > 0:
                self.y_speed = 0
                self.rect.bottom = p.rect.top
            if self.y_speed < 0:
                self.y_speed = 0
                self.rect.top = max(self.rect.top, p.rect.bottom)

class Enemy(GameSprite):
    def __init__(self, picture, width, height, x, y, speed):
        super().__init__(picture, width, height, x, y)
        self.speed = speed
        self.direction = 1  # 1 for right/down, -1 for left/up

    def update(self, barriers):
        self.rect.x += self.speed * self.direction
        # Check for wall collisions
        if pygame.sprite.spritecollideany(self, barriers):
            self.direction *= -1  # Change direction on collision
            self.rect.x += self.speed * self.direction
# Create wall sprites
walls = [
    GameSprite('9e8e240693123e6.png', 600, 1, 0, 0),
    GameSprite('9e8e240693123e6.png', 1, 600, 0, 0),
    GameSprite('9e8e240693123e6.png', 1, 600, 600, 0),
    GameSprite('9e8e240693123e6.png', 600, 1, 0, 600),
    GameSprite('9e8e240693123e6.png', 10, 70, 100, 1),
    GameSprite('9e8e240693123e6.png', 10, 100, 200, 100),
    GameSprite('9e8e240693123e6.png', 210, 10, 0, 200), 
    GameSprite('9e8e240693123e6.png', 10, 70, 500, 2),
    GameSprite('9e8e240693123e6.png', 10, 110, 550, 100),
    GameSprite('9e8e240693123e6.png', 10, 70, 500, 450),
    GameSprite('9e8e240693123e6.png', 10, 70, 350, 550),
    GameSprite('9e8e240693123e6.png', 10, 70, 150, 450),
    GameSprite('9e8e240693123e6.png', 10, 50, 70, 300),
    GameSprite('9e8e240693123e6.png', 10, 50, 260, 350),
    GameSprite('9e8e240693123e6.png', 10, 50, 350, 400),
    GameSprite('9e8e240693123e6.png', 400, 10, 100, 450)
]

enemyes = [
    Enemy('goomba.png', 50, 50, 100, 10, 15),
    Enemy('goomba.png', 50, 50, 400, 100, 15),
    Enemy('goomba.png', 50, 50, 250, 150, 15),
    Enemy('goomba.png', 50, 50, 100, 300, 15),
    Enemy('goomba.png', 50, 50, 300, 400, 15),
    Enemy('goomba.png', 50, 50, 400, 400, 5),
    Enemy('goomba.png', 50, 50, 350, 350, 10),
    Enemy('goomba.png', 50, 50, 200, 350, 15),
    Enemy('goomba.png', 50, 50, 250, 470, 5),
    Enemy('goomba.png', 50, 50, 90, 470, 5)
]





# Create player sprite
player = Player('837e6aab0cf63cc.png', 40, 40, 50, 50)

# Create a finish line sprite
final = GameSprite('greb.png', 40, 40, 50, 550)  # You will need to provide your finish line image

# Initialize font for future use in the game
font.init()
font = font.SysFont('Arial', 70)
win = font.render('YOU WIN', True, (255, 215, 0))
go = font.render('GAME OVER', True, (255, 0, 0))

# Initialize finish variable
finish = False

# Main game loop
run = True
while run:
    time.delay(50)
    window.blit(background, (0, 0))

    # Event handling
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_a:
                player.x_speed = -6
            elif e.key == K_d:
                player.x_speed = 6
            elif e.key == K_w:
                player.y_speed = -6
            elif e.key == K_s:
                player.y_speed = 6
        elif e.type == KEYUP:
            if e.key in (K_a, K_d):
                player.x_speed = 0
            if e.key in (K_w, K_s):
                player.y_speed = 0

    if finish != True:
        window.blit(background, (0, 0))
        player.update(walls)  # Обновление игрока
        player.reset()         # Отрисовка игрока

        if sprite.collide_rect(player, final):
            finish = True
            window.blit(win, (200, 300))

        for wall in walls:
            wall.reset()
        
        for enemy in enemyes:
            enemy.update(walls)  # Обновление позиций враговы
            enemy.reset()   
        if sprite.spritecollideany(player, enemyes):
            finish = True
            window.blit(go, (200, 300))
        final.reset()
    display.update()
pygame.quit()