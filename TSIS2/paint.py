import pygame
import datetime
from collections import deque

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Advanced")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(BLACK)

palette = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (255, 165, 0), (255, 255, 255)
]

color = (0, 0, 255)
tool = 'brush'


SIZES = [2, 5, 10]
T = 5

brush_radius = 10
drawing = False
start_pos = (0, 0)
current_pos = (0, 0)
prev_pos = None 

text_active = False   
text_pos = (0, 0)      
text_buffer = ""      
font = pygame.font.SysFont(None, 24)
text_font = pygame.font.SysFont(None, 32) 

def flood_fill(surface, pos, fill_color):
    x, y = pos
    target = surface.get_at((x, y))[:3] 
    if target == fill_color:
        return                            

    queue = deque()
    queue.append((x, y))
    visited = set()
    visited.add((x, y))

    while queue:
        cx, cy = queue.popleft()
        if surface.get_at((cx, cy))[:3] != target:
            continue
        surface.set_at((cx, cy), fill_color)

        for nx, ny in ((cx+1,cy),(cx-1,cy),(cx,cy+1),(cx,cy-1)):
            if (nx, ny) not in visited and 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                visited.add((nx, ny))
                queue.append((nx, ny))


def draw_shape(surface, tool, color, start, end, thickness):

    if tool == 'line':
        pygame.draw.line(surface, color, start, end, thickness)

    elif tool == 'rect':
        pygame.draw.rect(surface, color, (
            min(start[0], end[0]), min(start[1], end[1]),
            abs(start[0]-end[0]),  abs(start[1]-end[1])
        ), thickness)

    elif tool == 'circle':
        r = int(((start[0]-end[0])**2 + (start[1]-end[1])**2)**0.5)
        pygame.draw.circle(surface, color, start, r, thickness)

    elif tool == 'square':
        side = int(((start[0]-end[0])**2 + (start[1]-end[1])**2)**0.5)
        pygame.draw.rect(surface, color, (start[0], start[1], side, side), thickness)

    elif tool == 'right_triangle':
        dx, dy = end[0]-start[0], end[1]-start[1]
        pygame.draw.polygon(surface, color, [
            start,
            (start[0],       start[1]+dy),
            (start[0]+dx,    start[1]+dy)
        ], thickness)

    elif tool == 'equilateral_triangle':
        x1, y1 = start
        x2, y2 = end
        w = abs(x2-x1)
        h = int(w * (3**0.5) / 2)
        cx = (x1+x2)//2
        if y2 > y1:
            pts = [(cx, y1), (x1, y1+h), (x2, y1+h)]
        else:
            pts = [(cx, y1), (x1, y1-h), (x2, y1-h)]
        pygame.draw.polygon(surface, color, pts, thickness)

    elif tool == 'rhombus':
        cx = (start[0]+end[0])//2
        cy = (start[1]+end[1])//2
        hw = abs(end[0]-start[0])//2
        hh = abs(end[1]-start[1])//2
        pygame.draw.polygon(surface, color, [
            (cx, cy-hh), (cx+hw, cy), (cx, cy+hh), (cx-hw, cy)
        ], thickness)


TOOLBAR_H = 90   

def draw_toolbar():

    for i, c in enumerate(palette):
        pygame.draw.rect(screen, c, (10 + i*50, 10, 40, 40))

  
    size_labels = [("S", SIZES[0]), ("M", SIZES[1]), ("L", SIZES[2])]
    for i, (label, val) in enumerate(size_labels):
        bx = 320 + i*50
        col = WHITE if T == val else (120, 120, 120)
        pygame.draw.rect(screen, col, (bx, 10, 40, 40), 2)
        lbl = font.render(label, True, col)
        screen.blit(lbl, (bx+13, 18))

  
    info = font.render(f"Tool: {tool}  |  T={T}  (scroll to change)", True, WHITE)
    screen.blit(info, (10, 62))

 
    hints = font.render(
        "1Pencil 2Line 3Rect 4Circle 5Eraser 6Square 7RTri 8EqTri 9Rhombus 0Fill T=text  Ctrl+S=Save",
        True, (180, 180, 180)
    )
    screen.blit(hints, (10, 80))   



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:

            if text_active:
                if event.key == pygame.K_RETURN:
                    rendered = text_font.render(text_buffer, True, color)
                    canvas.blit(rendered, text_pos)
                    text_active = False
                    text_buffer = ""
                elif event.key == pygame.K_ESCAPE:
                    text_active = False
                    text_buffer = ""
                elif event.key == pygame.K_BACKSPACE:
                    text_buffer = text_buffer[:-1]
                else:
                    if event.unicode:
                        text_buffer += event.unicode

            else:
                if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    fname = f"canvas_{ts}.png"
                    pygame.image.save(canvas, fname)
                    print(f"Saved: {fname}")

                elif event.key == pygame.K_1: tool = 'pencil'
                elif event.key == pygame.K_2: tool = 'line'
                elif event.key == pygame.K_3: tool = 'rect'
                elif event.key == pygame.K_4: tool = 'circle'
                elif event.key == pygame.K_5: tool = 'eraser'
                elif event.key == pygame.K_6: tool = 'square'
                elif event.key == pygame.K_7: tool = 'right_triangle'
                elif event.key == pygame.K_8: tool = 'equilateral_triangle'
                elif event.key == pygame.K_9: tool = 'rhombus'
                elif event.key == pygame.K_0: tool = 'fill'
                elif event.key == pygame.K_t: tool = 'text'

                elif event.key == pygame.K_q: T = SIZES[0]
                elif event.key == pygame.K_w: T = SIZES[1]
                elif event.key == pygame.K_e: T = SIZES[2]

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            for i, c in enumerate(palette):
                if 10 + i*50 <= x <= 50 + i*50 and 10 <= y <= 50:
                    color = c

            for i, val in enumerate(SIZES):
                bx = 320 + i*50
                if bx <= x <= bx+40 and 10 <= y <= 50:
                    T = val

            if event.button == 4: T += 1
            elif event.button == 5: T = max(1, T - 1)

            if event.button == 1 and y > TOOLBAR_H:

                if tool == 'fill':
                    flood_fill(canvas, (x, y), color)

                elif tool == 'text':
                    text_active = True
                    text_pos = (x, y)
                    text_buffer = ""

                else:
                    drawing = True
                    start_pos = (x, y)
                    current_pos = (x, y)
                    prev_pos = (x, y)

        if event.type == pygame.MOUSEMOTION:
            current_pos = event.pos

            if drawing:
                if tool == 'pencil':
                    pygame.draw.line(canvas, color, prev_pos, event.pos, T)
                    prev_pos = event.pos

                elif tool == 'eraser':
                    pygame.draw.circle(canvas, BLACK, event.pos, brush_radius)

                elif tool == 'brush':
                    pygame.draw.circle(canvas, color, event.pos, brush_radius)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                drawing = False
                if tool not in ('pencil', 'brush', 'eraser'):
                    draw_shape(canvas, tool, color, start_pos, event.pos, T)

    screen.fill(BLACK)
    screen.blit(canvas, (0, 0))

    if drawing and tool not in ('pencil', 'brush', 'eraser'):
        draw_shape(screen, tool, color, start_pos, current_pos, T)

    if text_active:
        preview = text_font.render(text_buffer + "|", True, color)
        screen.blit(preview, text_pos)

    draw_toolbar()      

    pygame.display.flip() 
    clock.tick(60) 
