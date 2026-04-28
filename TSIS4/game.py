import pygame, random, time
from pygame.locals import *
from config import *
import settings as cfg

font_hud = None

def init_font():
    global font_hud
    font_hud = pygame.font.SysFont("times new roman", 20)


def random_cell(exclude=[]):
    while True:
        x = random.randrange(1, (WIN_W // CELL) - 1) * CELL
        y = random.randrange(1, (WIN_H // CELL) - 1) * CELL
        if [x, y] not in exclude:
            return [x, y]

def new_food(snake, obstacles):
    return random_cell(exclude=snake + obstacles)

def new_food_type():
    weights = [t[2] for t in FOOD_TYPES]
    return random.choices(FOOD_TYPES, weights=weights, k=1)[0]

def get_level(score):
    lvl = 0
    for i, (threshold, _) in enumerate(LEVELS):
        if score >= threshold:
            lvl = i
    return lvl

def spawn_obstacles(level, snake, existing=[]):
    if level < 2:   
        return []
    count = 4 + level * 2
    blocks = []
    for _ in range(count):
        pos = random_cell(exclude=snake + existing + blocks)
        blocks.append(pos)
    return blocks

def spawn_powerup(snake, obstacles, food_pos):
    kind = random.choice(list(POWERUP_COLORS.keys()))
    pos  = random_cell(exclude=snake + obstacles + [food_pos])
    return {"kind": kind, "pos": pos, "born": pygame.time.get_ticks()}

def draw_grid(screen):
    for x in range(0, WIN_W, CELL):
        pygame.draw.line(screen, pygame.Color(30,30,30), (x,0), (x,WIN_H))
    for y in range(0, WIN_H, CELL):
        pygame.draw.line(screen, pygame.Color(30,30,30), (0,y), (WIN_W,y))

def show_hud(screen, score, level, time_left, food_color, personal_best, active_pu, pu_end):
    screen.blit(font_hud.render(f"Score: {score}",        True, WHITE),  (8, 4))
    screen.blit(font_hud.render(f"Best: {personal_best}", True, YELLOW), (8, 24))
    lbl = font_hud.render(f"Level: {level+1}", True, YELLOW)
    screen.blit(lbl, (WIN_W - lbl.get_width() - 8, 4))
    timer = font_hud.render(f"Food: {time_left}s", True, food_color)
    screen.blit(timer, (WIN_W//2 - timer.get_width()//2, 4))
    if active_pu:
        if active_pu == "shield":
            pu_surf = font_hud.render("SHIELD READY", True, POWERUP_COLORS["shield"])
        else:
            remaining = max(0, (pu_end - pygame.time.get_ticks()) // 1000)
            pu_surf = font_hud.render(f"{active_pu.upper()} {remaining}s", True, POWERUP_COLORS[active_pu])
        screen.blit(pu_surf, (WIN_W//2 - pu_surf.get_width()//2, 24))

def show_level_up(screen, level):
    font = pygame.font.SysFont("times new roman", 42)
    surf = font.render(f"  Level {level+1}!  ", True, BLACK, YELLOW)
    screen.blit(surf, surf.get_rect(center=(WIN_W//2, WIN_H//2)))
    pygame.display.flip()
    time.sleep(0.4)


def run_game(screen, sound, snake_color, personal_best):
    init_font()
    fps = pygame.time.Clock()

    snake_pos  = [100, 50]
    snake_body = [[100,50],[90,50],[80,50],[70,50]]
    direction  = "RIGHT"
    change_to  = "RIGHT"

    score         = 0
    current_level = 0
    snake_speed   = LEVELS[0][1]

    obstacles      = []
    food_pos       = new_food(snake_body, obstacles)
    food_color, food_pts, _, food_life = new_food_type()
    food_born      = time.time()
    food_spawned   = True

    poison_pos     = new_food(snake_body + [food_pos], obstacles)
    poison_spawned = True

    powerup        = None 
    POWERUP_EVENT  = USEREVENT + 1
    pygame.time.set_timer(POWERUP_EVENT, 7000)  

    active_pu     = None    
    active_pu_end = 0      
    shield_active = False

    s_color = pygame.Color(*snake_color)

    while True:
        fps.tick(snake_speed)

        for event in pygame.event.get():
            if event.type == QUIT:
                return score, current_level + 1, "quit"
            if event.type == KEYDOWN:
                if event.key == K_UP:    change_to = "UP"
                if event.key == K_DOWN:  change_to = "DOWN"
                if event.key == K_LEFT:  change_to = "LEFT"
                if event.key == K_RIGHT: change_to = "RIGHT"
            if event.type == POWERUP_EVENT and powerup is None and active_pu is None:
                powerup = spawn_powerup(snake_body, obstacles, food_pos)

        if change_to == "UP"    and direction != "DOWN":  direction = "UP"
        if change_to == "DOWN"  and direction != "UP":    direction = "DOWN"
        if change_to == "LEFT"  and direction != "RIGHT": direction = "LEFT"
        if change_to == "RIGHT" and direction != "LEFT":  direction = "RIGHT"

        if direction == "UP":    snake_pos[1] -= CELL
        if direction == "DOWN":  snake_pos[1] += CELL
        if direction == "LEFT":  snake_pos[0] -= CELL
        if direction == "RIGHT": snake_pos[0] += CELL

        snake_body.insert(0, list(snake_pos))

        if snake_pos == food_pos:
            score      += food_pts
            if sound: pygame.mixer.Sound("assets/eat.mp3").play()
            food_spawned = False
        else:
            snake_body.pop()

        elapsed   = time.time() - food_born
        if not food_spawned or elapsed >= food_life:
            food_pos   = new_food(snake_body + [poison_pos] + obstacles, [])
            food_color, food_pts, _, food_life = new_food_type()
            food_born  = time.time()
            food_spawned = True

        if snake_pos == poison_pos:
            if sound: pygame.mixer.Sound("assets/faaah.mp3").play()
            snake_body = snake_body[:-2] if len(snake_body) > 2 else snake_body[:1]
            if len(snake_body) <= 1:
                return score, current_level + 1, "dead"
            poison_pos = new_food(snake_body + [food_pos] + obstacles, [])

        if powerup and snake_pos == powerup["pos"]:
            active_pu     = powerup["kind"]
            active_pu_end = pygame.time.get_ticks() + POWERUP_DURATION
            if active_pu == "speed":  snake_speed = int(LEVELS[current_level][1] * 1.6)
            if active_pu == "slow":   snake_speed = max(4, LEVELS[current_level][1] // 2)
            if active_pu == "shield": shield_active = True
            powerup = None

        if powerup and pygame.time.get_ticks() - powerup["born"] > POWERUP_LIFETIME:
            powerup = None

        if active_pu and active_pu != "shield" and pygame.time.get_ticks() > active_pu_end:
            snake_speed = LEVELS[current_level][1]
            active_pu   = None

        new_lvl = get_level(score)
        if new_lvl != current_level:
            current_level = new_lvl
            obstacles      = spawn_obstacles(current_level, snake_body, obstacles)
            snake_speed   = LEVELS[current_level][1]
            show_level_up(screen, current_level)

        s = cfg.load()
        screen.fill(BLACK)
        if s["grid"]: draw_grid(screen)

        for pos in snake_body:
            pygame.draw.rect(screen, s_color, pygame.Rect(pos[0], pos[1], CELL, CELL))

        pygame.draw.rect(screen, food_color,  pygame.Rect(food_pos[0],   food_pos[1],   CELL, CELL))
        pygame.draw.rect(screen, DARK_RED,    pygame.Rect(poison_pos[0], poison_pos[1], CELL, CELL))

        for ob in obstacles:
            pygame.draw.rect(screen, GRAY, pygame.Rect(ob[0], ob[1], CELL, CELL))

        if powerup:
            size = CELL * 1.5
            offset = (size - CELL) / 2
            pygame.draw.rect(screen, POWERUP_COLORS[powerup["kind"]],
                             pygame.Rect(powerup["pos"][0] - offset,
                                         powerup ["pos"][1] - offset,
                                         size, size))

        if shield_active:
            pygame.draw.rect(screen, pygame.Color(0,255,150),
                             pygame.Rect(snake_pos[0]-2, snake_pos[1]-2, CELL+4, CELL+4), 2)

        time_left = max(0, int(food_life - elapsed))
        show_hud(screen, score, current_level, time_left, food_color, personal_best, active_pu, active_pu_end)
        pygame.display.update()

        if snake_pos[0] < 0 or snake_pos[0] >= WIN_W or snake_pos[1] < 0 or snake_pos[1] >= WIN_H:
            if shield_active:
                shield_active = False
                active_pu     = None
                if direction == "RIGHT": snake_pos[0] = WIN_W - CELL
                if direction == "LEFT":  snake_pos[0] = 0
                if direction == "UP":    snake_pos[1] = 0
                if direction == "DOWN":  snake_pos[1] = WIN_H - CELL
                snake_body[0] = list(snake_pos)
            else:
                return score, current_level + 1, "dead"

        if snake_pos in snake_body[1:]:
            if shield_active:
                shield_active = False
                active_pu     = None
            else:
                return score, current_level + 1, "dead"

        if snake_pos in obstacles:
            if shield_active:
                shield_active = False
                active_pu     = None
                snake_body.pop()
            else:
                return score, current_level + 1, "dead"
