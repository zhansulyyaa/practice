import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Advanced")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Canvas is what we draw on permanently
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(BLACK)

palette = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (255, 165, 0), (255, 255, 255)
]

color = (0, 0, 255)
tool = 'brush'
#thickness
T = 5
brush_radius = 10
drawing = False
start_pos = (0, 0)
current_pos = (0, 0)   # tracks mouse position while dragging

font = pygame.font.SysFont(None, 24)


def draw_shape(surface, tool, color, start, end, thickness):
    """Draw the selected shape from start to end on the given surface."""

    if tool == 'rect':
        pygame.draw.rect(surface, color, (
            min(start[0], end[0]),
            min(start[1], end[1]),
            abs(start[0] - end[0]),
            abs(start[1] - end[1])
        ), thickness)

    elif tool == 'circle':
        r = int(((start[0]-end[0])**2 + (start[1]-end[1])**2)**0.5)
        pygame.draw.circle(surface, color, start, r, thickness)

    elif tool == 'square':
        side = int(((start[0]-end[0])**2 + (start[1]-end[1])**2)**0.5)
        pygame.draw.rect(surface, color, (start[0], start[1], side, side), thickness)

    elif tool == 'right_triangle':
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        p1 = start
        p2 = (start[0],        start[1] + dy)
        p3 = (start[0] + dx,   start[1] + dy)
        pygame.draw.polygon(surface, color, [p1, p2, p3], thickness)

    elif tool == 'equilateral_triangle':
        x1, y1 = start
        x2, y2 = end
        width = abs(x2 - x1)
        height = int(width * (3**0.5) / 2)
        cx = (x1 + x2) // 2
        if y2 > y1:
            p1 = (cx, y1)
            p2 = (x1, y1 + height)
            p3 = (x2, y1 + height)
        else:
            p1 = (cx, y1)
            p2 = (x1, y1 - height)
            p3 = (x2, y1 - height)
        pygame.draw.polygon(surface, color, [p1, p2, p3], thickness)

    elif tool == 'rhombus':
        cx  = (start[0] + end[0]) // 2
        cy  = (start[1] + end[1]) // 2
        hw  = abs(end[0] - start[0]) // 2
        hh  = abs(end[1] - start[1]) // 2
        pygame.draw.polygon(surface, color, [
            (cx,      cy - hh),
            (cx + hw, cy),
            (cx,      cy + hh),
            (cx - hw, cy)
        ], thickness)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Tool hotkeys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: tool = 'brush'
            elif event.key == pygame.K_2: tool = 'rect'
            elif event.key == pygame.K_3: tool = 'circle'
            elif event.key == pygame.K_4: tool = 'eraser'
            elif event.key == pygame.K_5: tool = 'square'
            elif event.key == pygame.K_6: tool = 'right_triangle'
            elif event.key == pygame.K_7: tool = 'equilateral_triangle'
            elif event.key == pygame.K_8: tool = 'rhombus'

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Color palette click (top bar)
            for i, c in enumerate(palette):
                if 10 + i*50 <= x <= 50 + i*50 and 10 <= y <= 50:
                    color = c

            if event.button == 1:
                drawing = True
                start_pos = event.pos
                current_pos = event.pos

            elif event.button == 4:
                T += 1
            elif event.button == 5:
                T = max(1, T - 1)

        if event.type == pygame.MOUSEMOTION:
            current_pos = event.pos   # always track mouse

            if drawing:
                if tool == 'brush':
                    pygame.draw.circle(canvas, color, event.pos, brush_radius)
                elif tool == 'eraser':
                    pygame.draw.circle(canvas, BLACK, event.pos, brush_radius)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False
                # Commit the final shape
                draw_shape(canvas, tool, color, start_pos, event.pos, T)

    screen.fill(BLACK)
    screen.blit(canvas, (0, 0))   # draw the permanent canvas

    # Draw live preview on top of canvas 
    if drawing and tool not in ('brush', 'eraser'):
        draw_shape(screen, tool, color, start_pos, current_pos, T)

    # Color palette
    for i, c in enumerate(palette):
        pygame.draw.rect(screen, c, (10 + i*50, 10, 40, 40))

    # Tool label
    text = font.render(f"Tool: {tool}  |  T={T}", True, WHITE)
    screen.blit(text, (10, 60))

    pygame.display.flip()
    clock.tick(60)
