import pygame
from persistence import load_leaderboard, load_settings, save_settings

WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
GRAY   = (60,  60,  60)
YELLOW = (255, 215, 0)
RED    = (220, 50,  50)
GREEN  = (0,   200, 80)

font_big   = pygame.font.SysFont("Verdana", 48)
font_med   = pygame.font.SysFont("Verdana", 26)
font_small = pygame.font.SysFont("Verdana", 20)

def button(screen, text, x, y, w=200, h=50, color=GRAY):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=8)
    lbl = font_med.render(text, True, WHITE)
    screen.blit(lbl, (x + (w - lbl.get_width())//2, y + (h - lbl.get_height())//2))
    return rect

def main_menu(screen):
    W, H = screen.get_size()
    while True:
        screen.fill(BLACK)
        title = font_big.render("RACER", True, YELLOW)
        screen.blit(title, ((W - title.get_width())//2, 70))

        b_play = button(screen, "Play",        W//2-100, 180)
        b_lb   = button(screen, "Leaderboard", W//2-100, 250)
        b_set  = button(screen, "Settings",    W//2-100, 320)
        b_quit = button(screen, "Quit",        W//2-100, 390, color=(150,30,30))

        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:            return "quit"
            if e.type == pygame.MOUSEBUTTONDOWN:
                if b_play.collidepoint(e.pos):   return "play"
                if b_lb.collidepoint(e.pos):     return "leaderboard"
                if b_set.collidepoint(e.pos):    return "settings"
                if b_quit.collidepoint(e.pos):   return "quit"

def enter_name(screen):
    W, H = screen.get_size()
    name = ""
    while True:
        screen.fill(BLACK)
        screen.blit(font_med.render("Enter your name:", True, WHITE), (W//2-130, 220))
        # name input box
        box = pygame.Rect(W//2-100, 270, 200, 45)
        pygame.draw.rect(screen, GRAY, box, border_radius=6)
        pygame.draw.rect(screen, WHITE, box, 2, border_radius=6)
        screen.blit(font_med.render(name + "|", True, YELLOW), (box.x+8, box.y+8))
        screen.blit(font_small.render("Press ENTER to start", True, GRAY), (W//2-110, 340))
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT: return "Player"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and name.strip(): return name.strip()
                elif e.key == pygame.K_BACKSPACE: name = name[:-1]
                elif len(name) < 14: name += e.unicode

def leaderboard_screen(screen):
    W, H = screen.get_size()
    board = load_leaderboard()
    while True:
        screen.fill(BLACK)
        screen.blit(font_big.render("TOP 10", True, YELLOW), (W//2-80, 30))
        for i, row in enumerate(board):
            txt = f"{i+1}. {row['name']}  {row['score']} pts  {row['distance']}m"
            screen.blit(font_small.render(txt, True, WHITE if i > 0 else YELLOW), (20, 100 + i*40))
        b_back = button(screen, "Back", W//2-100, H-80)
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return
            if e.type == pygame.MOUSEBUTTONDOWN:
                if b_back.collidepoint(e.pos): return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE: return

def settings_screen(screen):
    W, H = screen.get_size()
    s = load_settings()
    colors = ["red", "blue", "green", "yellow"]
    diffs  = ["easy", "normal", "hard"]

    while True:
        screen.fill(BLACK)
        screen.blit(font_big.render("Settings", True, YELLOW), (W//2-110, 30))

        # show current values and buttons to cycle them
        screen.blit(font_med.render(f"Sound: {'ON' if s['sound'] else 'OFF'}", True, WHITE), (20, 130))
        b_snd = button(screen, "Toggle", W-160, 125, w=140, h=40)

        screen.blit(font_med.render(f"Car: {s['car_color']}", True, WHITE), (20, 200))
        b_col = button(screen, "Change", W-160, 195, w=140, h=40)

        screen.blit(font_med.render(f"Difficulty: {s['difficulty']}", True, WHITE), (20, 270))
        b_dif = button(screen, "Change", W-160, 265, w=140, h=40)

        b_back = button(screen, "Save & Back", W//2-100, H-90, color=(0,150,50))
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                save_settings(s); return s
            if e.type == pygame.MOUSEBUTTONDOWN:
                if b_snd.collidepoint(e.pos):
                    s["sound"] = not s["sound"]
                if b_col.collidepoint(e.pos):
                    s["car_color"] = colors[(colors.index(s["car_color"]) + 1) % len(colors)]
                if b_dif.collidepoint(e.pos):
                    s["difficulty"] = diffs[(diffs.index(s["difficulty"]) + 1) % len(diffs)]
                if b_back.collidepoint(e.pos):
                    save_settings(s); return s

def game_over_screen(screen, score, distance, coins):
    W, H = screen.get_size()
    while True:
        screen.fill(BLACK)
        screen.blit(font_big.render("GAME OVER", True, RED), (W//2-150, 80))
        screen.blit(font_med.render(f"Score:    {score}",     True, WHITE), (W//2-100, 190))
        screen.blit(font_med.render(f"Distance: {distance}m", True, WHITE), (W//2-100, 240))
        screen.blit(font_med.render(f"Coins:    {coins}",     True, YELLOW),(W//2-100, 290))
        b_retry = button(screen, "Retry",     W//2-100, 370, color=(0,150,50))
        b_menu  = button(screen, "Main Menu", W//2-100, 440)
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:                        return "quit"
            if e.type == pygame.MOUSEBUTTONDOWN:
                if b_retry.collidepoint(e.pos):              return "retry"
                if b_menu.collidepoint(e.pos):               return "menu"
