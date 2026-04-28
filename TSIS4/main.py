import pygame, sys
from config import *
import settings as cfg
from db import setup, get_or_create_player, save_session, get_personal_best
from ui import init_fonts, main_menu, leaderboard_screen, settings_screen, game_over_screen
from game import run_game

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption("Snake")

setup()
init_fonts()

s = cfg.load()

while True:
    action, username = main_menu(screen)

    if action == "quit":
        pygame.quit(); sys.exit()

    elif action == "leaderboard":
        leaderboard_screen(screen)

    elif action == "settings":
        s = settings_screen(screen)

    elif action == "play":
        player_id = get_or_create_player(username)
        best      = get_personal_best(player_id)

        while True:
            sound       = s["sound"]
            snake_color = s["snake_color"]

            score, level, result = run_game(screen, sound, snake_color, best)

            if result == "quit":
                pygame.quit(); sys.exit()

            save_session(player_id, score, level)
            best = get_personal_best(player_id)

            outcome = game_over_screen(screen, score, level, best)

            if outcome == "retry": continue
            if outcome == "menu":  break
            if outcome == "quit":
                pygame.quit(); sys.exit()
