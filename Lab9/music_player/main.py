import pygame
import os

pygame.init()
pygame.mixer.init()

music_folder = r'/Users/zansezim/Practice/Lab9/music_player/music'
songs = [os.path.join(music_folder, f) for f in os.listdir(music_folder) 
         if f.endswith(('.mp3', '.wav'))]

if not songs:
    print("No .mp3 or .wav files found in", music_folder)
    pygame.quit()
    exit()

durations = []
for song in songs:
    durations.append(pygame.mixer.Sound(song).get_length())     # adds the song length from music folder

music_index = 0
num = len(songs)

screen = pygame.display.set_mode((1200, 700))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
cur_pos = 0             #defining

font = pygame.font.SysFont(None, 36)

p_text = font.render('P = Play', True, BLACK)
s_text = font.render('S = Stop', True, BLACK)      
n_text = font.render('N = Next track', True, BLACK)
b_text = font.render('B = Previous (Back)', True, BLACK)
q_text = font.render('Q = Quit', True, BLACK)

done = False

clock = pygame.time.Clock()

def play_next():
    global music_index
    music_index = (music_index + 1) % num
    pygame.mixer.music.load(songs[music_index])
    pygame.mixer.music.play()

def play_prev():
    global music_index
    music_index = (music_index - 1) % num
    pygame.mixer.music.load(songs[music_index])
    pygame.mixer.music.play()       #taking the index and playing it 

def get_start(h, m, s):
    # pad with 0, 2 characters wide, 0 decimal places
    time_str = f"{h:02.0f}:{m:02.0f}:{s:02.0f}"
    return font.render(time_str, True, BLACK)    # timings

current_times = 0

is_paused = False

while not done:
    if durations[music_index] > 0:                     # avoid division by zero
        progress_ratio = current_times / durations[music_index]
        circle_x = 200 + progress_ratio * 900
    else:
        circle_x = 200
    if pygame.mixer.music.get_busy():
        current_times = pygame.mixer.music.get_pos() / 1000
    screen.fill(WHITE)

    song_name = os.path.basename(songs[music_index])
    name_surface = font.render(f"{song_name}", True, BLACK)
    screen.blit(name_surface, (560, 350))

    screen.blit(p_text, (30, 50))
    screen.blit(s_text, (30, 80))
    screen.blit(n_text, (30, 110))
    screen.blit(b_text, (30, 140))
    screen.blit(q_text, (30, 170))
    w = 300
    for i, s in enumerate(songs, start=0):
        s0 = os.path.basename(s)
        if 50+30*i < 350:
            if s0 != song_name: 
                name = font.render(f'{i+1}. {s0}', True, BLACK)
                screen.blit(name, (300, 50+30*i))
            else:
                name = font.render(f'{i+1}. {s0}', True, (255,0,0))
                screen.blit(name, (300, 50+30*i))
        else:
            if s0 != song_name: 
                name = font.render(f'{i+1}. {s0}', True, BLACK)
                screen.blit(name, (450, 50+30*i))
            else:
                name = font.render(f'{i+1}. {s0}', True, (255,0,0))
                screen.blit(name, (450, 50+30*i))

    pygame.draw.line(screen, BLACK, (200, 450), (1100,450), 2)

    add = durations[music_index]/900

    h = current_times//3600
    m = current_times//60
    s = current_times%60

    start = get_start(h,m,s)
    end = get_start(durations[music_index]//3600, durations[music_index]//60, durations[music_index]%60)        
    # end = font.render(f"{durations[music_index]//3600:.0f}:{durations[music_index]//60:.0f}:{durations[music_index]%60:.0f}", True, BLACK)

    screen.blit(start, (210,420))
    screen.blit(end, (1050,420))

    pygame.draw.circle(screen, (255, 0, 0), (circle_x, 450), 7.5)
    pygame.draw.line(screen, (255, 0, 0), (200, 450), (circle_x,450), 2)

    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                done = True
            elif event.key == pygame.K_p:
                if is_paused:
                    pygame.mixer.music.unpause()
                    is_paused = False
                elif not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load(songs[music_index])
                    pygame.mixer.music.play()
                    pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
            elif event.key == pygame.K_s:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                    is_paused = True
            elif event.key == pygame.K_n:
                cur_pos = 0
                play_next()
                is_paused = False
            elif event.key == pygame.K_b:
                play_prev()
                is_paused = False
        elif event.type == pygame.USEREVENT + 1:
            play_next()       

    pygame.display.flip()
    clock.tick(15)  

pygame.quit()