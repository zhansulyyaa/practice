import pygame, sys
from persistence import load_settings, save_score

pygame.init()
pygame.mixer.init()


from ui import main_menu, enter_name, leaderboard_screen, settings_screen, game_over_screen
from racer import run_game

screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Racer")
sounds = {
    "crash":   pygame.mixer.Sound("sound/crash.mp3"),
    "coin":    pygame.mixer.Sound("sound/coin.mp3"),
    "powerup": pygame.mixer.Sound("sound/powerup.mp3"),
}

settings = load_settings()

def apply_music(s):
    if s["sound"]: pygame.mixer.music.play(-1)
    else:          pygame.mixer.music.stop()

apply_music(settings)

while True:
    action = main_menu(screen)

    if action == "quit":
        pygame.quit(); sys.exit()

    elif action == "leaderboard":
        leaderboard_screen(screen)

    elif action == "settings":
        settings = settings_screen(screen)
        apply_music(settings)

    elif action == "play":
        name = enter_name(screen)

        while True:
            score, distance, coins, result = run_game(screen, settings, sounds, name)

            if result == "quit":
                pygame.quit(); sys.exit()

            save_score(name, score, distance)

            outcome = game_over_screen(screen, score, distance, coins)

            if outcome == "retry": continue
            if outcome == "menu":  break
            if outcome == "quit":
                pygame.quit(); sys.exit()
