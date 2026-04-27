import pygame, sys
from pygame.locals import *
import random, time

pygame.init()
pygame.mixer.init()

FPS = 60
clock = pygame.time.Clock()

collision_sound = pygame.mixer.Sound("sound/crash.mp3")
coin_pickup_sound = pygame.mixer.Sound("sound/sonic.mp3")

RED = (255, 0, 0)   
BLACK = (0, 0, 0)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

SPEED = 5
SCORE = 0
COIN_SCORE = 0

COINS_PER_SPEED_UP = 5

# coin types with different weights: (point_value, color, size, weight)
# weight controls how often each type appears — higher = more common
COIN_TYPES = [
    (1,  (255, 215,   0), 20, 60),   # gold   – common,   worth 1
    (3,  (192, 192, 192), 22, 30),   # silver – uncommon, worth 3
    (5,  (0,   191, 255), 25, 10),   # blue   – rare,     worth 5
]

font_small = pygame.font.SysFont("Verdana", 20)
font_big = pygame.font.SysFont("Verdana", 60)
game_over = font_big.render("Game Over", True, BLACK)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

background = pygame.image.load("images/street.png").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 72))
        self.rect = self.image.get_rect()
        self.respawn()

    def respawn(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -100)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)

        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.respawn()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/car.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (44, 85))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)

        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        population = COIN_TYPES
        weights    = [t[3] for t in population]
        chosen     = random.choices(population, weights=weights, k=1)[0]   

        self.value = chosen[0]  
        size       = chosen[2]  

        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, chosen[1], (size // 2, size // 2), size // 2)

        self.rect = self.image.get_rect()
        self.respawn()

    def respawn(self):
        self.rect.center = (
            random.randint(40, SCREEN_WIDTH - 40),
            random.randint(-300, -50)
        )

    def move(self):
        self.rect.move_ip(0, 2)

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()  


player = Player()
enemy = Enemy()

enemies = pygame.sprite.Group(enemy)
coins = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)

COIN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(COIN_EVENT, 2000)


while True:

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == COIN_EVENT:
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)

    screen.blit(background, (0, 0))

    screen.blit(font_small.render(f"Score: {SCORE}", True, BLACK), (10, 10))
    screen.blit(font_small.render(f"Coins: {COIN_SCORE}", True, BLACK), (260, 10))

    for obj in all_sprites:
        screen.blit(obj.image, obj.rect)
        obj.move()

    if pygame.sprite.spritecollideany(player, enemies):
        screen.fill(RED)
        collision_sound.play()
        screen.blit(game_over, (30, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    hits = pygame.sprite.spritecollide(player, coins, True)
    if hits:
        for coin in hits:
            COIN_SCORE += coin.value
        coin_pickup_sound.play()

        SPEED = 5 + (COIN_SCORE // COINS_PER_SPEED_UP)

    pygame.display.update()
    clock.tick(FPS)
