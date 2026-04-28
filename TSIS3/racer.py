import pygame, random, time
from pygame.locals import *

WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)
BLUE   = (0,   150, 255)
GREEN  = (0,   200, 80)
RED    = (220, 50,  50)

W = 400
H = 600

font_small = pygame.font.SysFont("Verdana", 18)
font_med   = pygame.font.SysFont("Verdana", 22)

COIN_TYPES = [
    (1, YELLOW,          20, 60),
    (3, (192,192,192),   22, 30),
    (5, BLUE,            25, 10),
]

POWERUP_TYPES = [
    ("nitro",  ORANGE),
    ("shield", BLUE),
    ("repair", GREEN),
]


class Player(pygame.sprite.Sprite):
    def __init__(self, car_color):
        super().__init__()
        img_map = {
            "red":    "images/car_red.png",
            "blue":   "images/car_blue.png",
            "green":  "images/car_green.png",
            "yellow": "images/car_yellow.png",
        }
        self.image = pygame.image.load(img_map.get(car_color, "images/car_red.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (44, 85))
        self.rect  = self.image.get_rect()
        self.rect.center = (W // 2, 520)
        self.shield = False 
        self.nitro  = False  
        self.nitro_end = 0

    def move(self):
        keys  = pygame.key.get_pressed()
        speed = 8 if self.nitro else 5
        if keys[K_LEFT]  and self.rect.left  > 0: self.rect.x -= speed
        if keys[K_RIGHT] and self.rect.right < W: self.rect.x += speed
        if self.nitro and time.time() > self.nitro_end:
            self.nitro = False


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.image.load("images/enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 72))
        self.rect  = self.image.get_rect()
        self.speed = speed
        self.rect.center = (random.randint(40, W - 40), random.randint(-300, -80))

    def update(self):
        self.rect.y += 15
        if self.rect.top > H:
            self.rect.center = (random.randint(40, W - 40), random.randint(-300, -80))


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        weights = [t[3] for t in COIN_TYPES]
        chosen  = random.choices(COIN_TYPES, weights=weights, k=1)[0]
        self.value = chosen[0]
        size = chosen[2]
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, chosen[1], (size//2, size//2), size//2)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, W - 40), random.randint(-300, -50))

    def update(self):
        self.rect.y += 3
        if self.rect.top > H:
            self.kill()


class Obstacle(pygame.sprite.Sprite):
    TYPES = [
        ((50, 20), (30, 30, 30)),   
        ((30, 30), (60, 40, 10)),    
    ]
    def __init__(self):
        super().__init__()
        size, color = random.choice(self.TYPES)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill(color)
        self.rect  = self.image.get_rect()
        self.rect.center = (random.randint(40, W - 40), -60)

    def update(self):
        self.rect.y += 4
        if self.rect.top > H:
            self.kill()


class Barrier(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 50), pygame.SRCALPHA)
        self.image.fill((255, 80, 0))
        self.rect  = self.image.get_rect()
        self.rect.center = (random.randint(60, W - 60), -60)
        self.dx = random.choice([-2, 2])   

    def update(self):
        self.rect.x += self.dx
        self.rect.y += 4
        if self.rect.left < 0 or self.rect.right > W:
            self.dx = -self.dx
        if self.rect.top > H:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        kind, color = random.choice(POWERUP_TYPES)
        self.kind  = kind
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(self.image, color, (0, 0, 32, 32), border_radius=6)
        lbl = pygame.font.SysFont("Verdana", 16, bold=True).render(kind[0].upper(), True, WHITE)
        self.image.blit(lbl, (9, 7))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, W - 40), -60)
        self.born = time.time()   

    def update(self):
        self.rect.y += 2
      
        if self.rect.top > H or time.time() - self.born > 12:
            self.kill()


def run_game(screen, settings, sounds, player_name):
    background = pygame.image.load("images/street.png").convert()
    background = pygame.transform.scale(background, (W, H))

    base_speed = {"easy": 4, "normal": 6, "hard": 9}[settings["difficulty"]]
    speed = base_speed

    score      = 0
    coin_score = 0
    distance   = 0
    bg_y       = 0   

    active_pu     = None  
    active_pu_end = 0     

    clock = pygame.time.Clock()

    player   = Player(settings["car_color"])
    enemies  = pygame.sprite.Group()
    coins    = pygame.sprite.Group()
    obstacles= pygame.sprite.Group()
    barriers = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    enemy_count = {"easy": 1, "normal": 2, "hard": 3}[settings["difficulty"]]
    for _ in range(enemy_count):
        enemies.add(Enemy(speed))

    COIN_EV    = USEREVENT + 1
    OBS_EV     = USEREVENT + 2
    BARRIER_EV = USEREVENT + 3
    POWER_EV   = USEREVENT + 4

    pygame.time.set_timer(COIN_EV,    2000)  
    pygame.time.set_timer(OBS_EV,     2500)   
    pygame.time.set_timer(BARRIER_EV, 6000)   
    pygame.time.set_timer(POWER_EV,   7000)   

    while True:
        clock.tick(30)
        distance += 1   

        for event in pygame.event.get():
            if event.type == QUIT:
                return score, distance//30, coin_score, "quit"
            if event.type == COIN_EV:
                coins.add(Coin())
            if event.type == OBS_EV:
                obstacles.add(Obstacle())
            if event.type == BARRIER_EV:
                barriers.add(Barrier())
            if event.type == POWER_EV and active_pu is None:
                powerups.add(PowerUp())

        bg_y = (bg_y + speed) % H
        screen.blit(background, (0, bg_y - H))
        screen.blit(background, (0, bg_y))

        player.move()
        enemies.update()
        coins.update()
        obstacles.update()
        barriers.update()
        powerups.update()

        for group in [enemies, coins, obstacles, barriers, powerups]:
            group.draw(screen)
        screen.blit(player.image, player.rect)

        if pygame.sprite.spritecollideany(player, enemies):
            if player.shield:
                player.shield = False
                active_pu = None
                pygame.sprite.spritecollide(player, enemies, True)
                enemies.add(Enemy(speed))   # respawn a new one
            else:
                if settings["sound"]: sounds["crash"].play()
                return score, distance//30, coin_score, "dead"

        if pygame.sprite.spritecollideany(player, barriers):
            if player.shield:
                player.shield = False
                active_pu = None
                pygame.sprite.spritecollide(player, barriers, True)
            else:
                if settings["sound"]: sounds["crash"].play()
                return score, distance//60, coin_score, "dead"

        if pygame.sprite.spritecollide(player, obstacles, True):
            if not player.shield:
                speed = max(base_speed, speed - 1)
                for e in enemies: e.speed = speed

        hits = pygame.sprite.spritecollide(player, coins, True)
        for coin in hits:
            coin_score += coin.value
            score      += coin.value
            if settings["sound"]: sounds["coin"].play()
        if hits:
            speed = base_speed + (coin_score // 5)
            for e in enemies: e.speed = speed

        pu_hit = pygame.sprite.spritecollide(player, powerups, True)
        for pu in pu_hit:
            if settings["sound"]: sounds["powerup"].play()
            active_pu     = pu.kind
            active_pu_end = time.time() + 5
            if pu.kind == "nitro":
                player.nitro     = True
                player.nitro_end = time.time() + 4
            elif pu.kind == "shield":
                player.shield = True
            elif pu.kind == "repair":
                speed = base_speed
                for e in enemies: e.speed = speed
                active_pu = None

        if active_pu and active_pu != "shield" and time.time() > active_pu_end:
            active_pu    = None
            player.nitro = False

        score += 1

        screen.blit(font_small.render(f"Score: {score}",       True, WHITE),  (10, 10))
        screen.blit(font_small.render(f"Coins: {coin_score}",  True, YELLOW), (W-130, 10))
        screen.blit(font_small.render(f"Dist: {distance//60}m",True, WHITE),  (10, 32))

        if active_pu:
            t = f"SHIELD" if active_pu == "shield" else f"{active_pu.upper()} {max(0, active_pu_end - time.time()):.1f}s"
            surf = font_med.render(t, True, ORANGE)
            screen.blit(surf, ((W - surf.get_width())//2, 10))

        if player.shield:
            pygame.draw.rect(screen, BLUE,   player.rect, 3, border_radius=4)
        if player.nitro:
            pygame.draw.rect(screen, ORANGE, player.rect, 3, border_radius=4)

        pygame.display.update()
