import pygame
import settings as cfg
from config import *
from db import get_top10

font_big   = None
font_med   = None
font_small = None

def init_fonts():
    global font_big, font_med, font_small
    font_big   = pygame.font.SysFont("times new roman", 48)
    font_med   = pygame.font.SysFont("times new roman", 28)
    font_small = pygame.font.SysFont("times new roman", 20)

def btn(screen, text, x, y, w=200, h=46, color=GRAY):
    """draw button, return rect"""
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, color, rect, border_radius=6)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=6)
    lbl = font_med.render(text, True, WHITE)
    screen.blit(lbl, (x + (w - lbl.get_width())//2, y + (h - lbl.get_height())//2))
    return rect

def main_menu(screen):
    W, H = screen.get_size()
    name = ""
    while True:
        screen.fill(BLACK)
        screen.blit(font_big.render("SNAKE", True, GREEN), (W//2 - 80, 50))
        screen.blit(font_med.render("Username:", True, WHITE), (W//2 - 100, 130))

        box = pygame.Rect(W//2 - 100, 165, 200, 40)
        pygame.draw.rect(screen, GRAY, box, border_radius=6)
        pygame.draw.rect(screen, WHITE, box, 2, border_radius=6)
        screen.blit(font_med.render(name + "|", True, YELLOW), (box.x + 6, box.y + 5))

        b_play = btn(screen, "Play",        W//2-100, 230)
        b_lb   = btn(screen, "Leaderboard", W//2-100, 290)
        b_set  = btn(screen, "Settings",    W//2-100, 350)
        b_quit = btn(screen, "Quit",        W//2-100, 410, color=pygame.Color(150,30,30))

        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:            return "quit", name
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE:  name = name[:-1]
                elif len(name) < 16:             name += e.unicode
            if e.type == pygame.MOUSEBUTTONDOWN:
                if b_play.collidepoint(e.pos) and name.strip(): return "play", name.strip()
                if b_lb.collidepoint(e.pos):   return "leaderboard", name
                if b_set.collidepoint(e.pos):  return "settings", name
                if b_quit.collidepoint(e.pos): return "quit", name

def leaderboard_screen(screen):
    W, H = screen.get_size()
    rows = get_top10()
    while True:
        screen.fill(BLACK)
        screen.blit(font_big.render("TOP 10", True, YELLOW), (W//2 - 90, 20))
        header = font_small.render("Rank  Name             Score  Lvl  Date", True, GRAY)
        screen.blit(header, (30, 80))
        for i, (uname, score, lvl, date) in enumerate(rows):
            color = YELLOW if i == 0 else WHITE
            line  = f"{i+1:<5} {uname:<16} {score:<6} {lvl:<4} {date}"
            screen.blit(font_small.render(line, True, color), (30, 108 + i*34))
        b_back = btn(screen, "Back", W//2-100, H-70)
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return
            if e.type == pygame.MOUSEBUTTONDOWN:
                if b_back.collidepoint(e.pos): return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:   return

def settings_screen(screen):
    W, H = screen.get_size()
    s = cfg.load()
    color_opts = [[0,200,0], [0,100,255], [255,200,0], [255,80,80]]
    color_names = ["Green", "Blue", "Yellow", "Red"]

    while True:
        screen.fill(BLACK)
        screen.blit(font_big.render("Settings", True, YELLOW), (W//2 - 110, 30))

        cur_color = s["snake_color"]
        cidx = color_opts.index(cur_color) if cur_color in color_opts else 0
        screen.blit(font_med.render(f"Snake color: {color_names[cidx]}", True, WHITE), (30, 130))
        pygame.draw.rect(screen, cur_color, pygame.Rect(W-80, 128, 40, 30))
        b_col = btn(screen, "Change", W-220, 128, w=130, h=36)

        screen.blit(font_med.render(f"Grid: {'ON' if s['grid'] else 'OFF'}", True, WHITE), (30, 200))
        b_grid = btn(screen, "Toggle", W-220, 198, w=130, h=36)

        screen.blit(font_med.render(f"Sound: {'ON' if s['sound'] else 'OFF'}", True, WHITE), (30, 270))
        b_snd = btn(screen, "Toggle", W-220, 268, w=130, h=36)

        b_back = btn(screen, "Save & Back", W//2-100, H-80, color=pygame.Color(0,150,50))
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                cfg.save(s); return s
            if e.type == pygame.MOUSEBUTTONDOWN:
                if b_col.collidepoint(e.pos):
                    s["snake_color"] = color_opts[(cidx + 1) % len(color_opts)]
                if b_grid.collidepoint(e.pos):
                    s["grid"] = not s["grid"]
                if b_snd.collidepoint(e.pos):
                    s["sound"] = not s["sound"]
                if b_back.collidepoint(e.pos):
                    cfg.save(s); return s

def game_over_screen(screen, score, level, personal_best):
    W, H = screen.get_size()
    while True:
        screen.fill(BLACK)
        screen.blit(font_big.render("GAME OVER", True, RED),    (W//2-160, 100))
        screen.blit(font_med.render(f"Score: {score}",          True, WHITE),  (W//2-100, 200))
        screen.blit(font_med.render(f"Level: {level}",          True, WHITE),  (W//2-100, 245))
        screen.blit(font_med.render(f"Best:  {personal_best}",  True, YELLOW), (W//2-100, 290))
        b_retry = btn(screen, "Retry",     W//2-100, 360, color=pygame.Color(0,150,50))
        b_menu  = btn(screen, "Main Menu", W//2-100, 420)
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:                        return "quit"
            if e.type == pygame.MOUSEBUTTONDOWN:
                if b_retry.collidepoint(e.pos):              return "retry"
                if b_menu.collidepoint(e.pos):               return "menu"
