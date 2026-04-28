import pygame


WIN_W = 720
WIN_H = 480
CELL  = 10


BLACK    = pygame.Color(0,   0,   0)
WHITE    = pygame.Color(255, 255, 255)
RED      = pygame.Color(255,  0,   0)
GREEN    = pygame.Color(0,  200,   0)
YELLOW   = pygame.Color(255, 215,  0)
ORANGE   = pygame.Color(255, 140,  0)
DARK_RED = pygame.Color(139,  0,   0)
PURPLE   = pygame.Color(180,  0, 180)
CYAN     = pygame.Color(0,  200, 255)
GRAY     = pygame.Color(80,  80,  80)

LEVELS = [
    (0,   10),
    (30,  14),
    (70,  18),
    (120, 23),
    (180, 28),
    (220, 40),
    (280, 50),
    (300, 100),
]

FOOD_TYPES = [
    (ORANGE, 10, 60, 20),
    (PURPLE, 20, 30, 15),
    (CYAN,   30, 10, 10),
]

POWERUP_COLORS = {
    "speed":  pygame.Color(255, 255,   0),
    "slow":   pygame.Color(100, 100, 255),
    "shield": pygame.Color(0,   255, 150),
}

POWERUP_DURATION = 5000   
POWERUP_LIFETIME = 12000   
