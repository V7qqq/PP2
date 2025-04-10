import pygame
import sys

pygame.init()

#настройка экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyPaint 🎨")
clock = pygame.time.Clock()

# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
current_color = BLACK

# переменные
radius = 5
mode = 'draw'  # draw, rect, circle, erase
start_pos = None
last_pos = None

#фон белый 
screen.fill(WHITE)

def drawLineBetween(surface, start, end, width, color): #функция для плавной отрисовки линий, линейная интерполяция
    #насколько далеко по X и Y расположены эти две точки.
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy)) #сколько шагов нужно сделать, чтобы отрисовать линию. Чем дальше точки, тем больше шагов что бы линия была палвной
    for i in range(iterations):
        progress = i / iterations #процент интерполяции
        x = int(start[0] * (1 - progress) + end[0] * progress)
        y = int(start[1] * (1 - progress) + end[1] * progress)
        pygame.draw.circle(surface, color, (x, y), width)

# цикл
import pygame
import sys

pygame.init()

# настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyPaint 🎨")
clock = pygame.time.Clock()

# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
current_color = BLACK

# переменные
radius = 5
mode = 'draw'  # draw, rect, circle, erase, square, right_triangle, equilateral_triangle, rhombus
start_pos = None
last_pos = None
screen.fill(WHITE)  # фон

def drawLineBetween(surface, start, end, width, color):
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    for i in range(iterations):
        progress = i / iterations
        x = int(start[0] * (1 - progress) + end[0] * progress)
        y = int(start[1] * (1 - progress) + end[1] * progress)
        pygame.draw.circle(surface, color, (x, y), width)

running = True
while running:
    pressed = pygame.key.get_pressed()
    ctrl = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # обработка клавиш
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_z:
                current_color = (255, 0, 0)
            elif event.key == pygame.K_x:
                current_color = (0, 255, 0)
            elif event.key == pygame.K_c:
                current_color = (0, 0, 255)
            elif event.key == pygame.K_b:
                current_color = BLACK
            elif event.key == pygame.K_n:
                current_color = WHITE
            elif event.key == pygame.K_1:
                mode = 'draw'
            elif event.key == pygame.K_2:
                mode = 'erase'
            elif event.key == pygame.K_3:
                mode = 'circle'
            elif event.key == pygame.K_4:
                mode = 'rect'
            elif event.key == pygame.K_5:
                mode = 'square'
            elif event.key == pygame.K_6:
                mode = 'right_triangle'
            elif event.key == pygame.K_7:
                mode = 'equilateral_triangle'
            elif event.key == pygame.K_8:
                mode = 'rhombus'

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            start_pos = event.pos
            temp_surface = screen.copy()

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and start_pos:
            end_pos = event.pos
            x1, y1 = start_pos
            x2, y2 = end_pos

            if mode == 'circle':
                center = ((x1 + x2) // 2, (y1 + y2) // 2)
                radius_circle = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5 / 2)
                pygame.draw.circle(screen, current_color, center, radius_circle, 2)
            elif mode == 'rect':
                rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
                pygame.draw.rect(screen, current_color, rect, 2)
            elif mode == 'square':
                side = min(abs(x2 - x1), abs(y2 - y1))
                rect = pygame.Rect(x1, y1, side * (1 if x2 > x1 else -1), side * (1 if y2 > y1 else -1))
                pygame.draw.rect(screen, current_color, rect, 2)
            elif mode == 'right_triangle':
                points = [(x1, y1), (x1, y2), (x2, y2)]
                pygame.draw.polygon(screen, current_color, points, 2)
            elif mode == 'equilateral_triangle':
                side = abs(x2 - x1)
                height = int((3**0.5 / 2) * side)
                direction = 1 if y2 > y1 else -1
                points = [(x1, y1), (x1 - side // 2, y1 + height * direction), (x1 + side // 2, y1 + height * direction)]
                pygame.draw.polygon(screen, current_color, points, 2)
            elif mode == 'rhombus':
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                dx = abs(x2 - x1) // 2
                dy = abs(y2 - y1) // 2
                points = [(center_x, center_y - dy), (center_x + dx, center_y),
                          (center_x, center_y + dy), (center_x - dx, center_y)]
                pygame.draw.polygon(screen, current_color, points, 2)

            start_pos = None

        if event.type == pygame.MOUSEMOTION:
            if event.buttons[0] and mode in ['draw', 'erase']:
                if last_pos:
                    drawLineBetween(screen, last_pos, event.pos, radius, WHITE if mode == 'erase' else current_color)
                last_pos = event.pos
            else:
                last_pos = None

            if event.buttons[0] and start_pos and mode in ['circle', 'rect', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus']:
                screen.blit(temp_surface, (0, 0))
                x1, y1 = start_pos
                x2, y2 = event.pos

                if mode == 'circle':
                    center = ((x1 + x2) // 2, (y1 + y2) // 2)
                    radius_circle = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5 / 2)
                    pygame.draw.circle(screen, current_color, center, radius_circle, 2)
                elif mode == 'rect':
                    rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
                    pygame.draw.rect(screen, current_color, rect, 2)
                elif mode == 'square':
                    side = min(abs(x2 - x1), abs(y2 - y1))
                    rect = pygame.Rect(x1, y1, side * (1 if x2 > x1 else -1), side * (1 if y2 > y1 else -1))
                    pygame.draw.rect(screen, current_color, rect, 2)
                elif mode == 'right_triangle':
                    points = [(x1, y1), (x1, y2), (x2, y2)]
                    pygame.draw.polygon(screen, current_color, points, 2)
                elif mode == 'equilateral_triangle':
                    side = abs(x2 - x1)
                    height = int((3**0.5 / 2) * side)
                    direction = 1 if y2 > y1 else -1
                    points = [(x1, y1), (x1 - side // 2, y1 + height * direction), (x1 + side // 2, y1 + height * direction)]
                    pygame.draw.polygon(screen, current_color, points, 2)
                elif mode == 'rhombus':
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    dx = abs(x2 - x1) // 2
                    dy = abs(y2 - y1) // 2
                    points = [(center_x, center_y - dy), (center_x + dx, center_y),
                              (center_x, center_y + dy), (center_x - dx, center_y)]
                    pygame.draw.polygon(screen, current_color, points, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

