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
running = True
while running:
    #обработка контрола
    pressed = pygame.key.get_pressed()
    ctrl = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
    #выход из игры
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #обработка клавиш
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_z:
                current_color = (255, 0, 0) #обработка цветов
            elif event.key == pygame.K_x:
                current_color = (0, 255, 0)
            elif event.key == pygame.K_c:
                current_color = (0, 0, 255)
            elif event.key == pygame.K_b:
                current_color = BLACK
            elif event.key == pygame.K_n:
                current_color = WHITE
            elif event.key == pygame.K_1: #смена модов
                mode = 'draw'
            elif event.key == pygame.K_3:
                mode = 'circle'
            elif event.key == pygame.K_2:
                mode = 'erase'
            elif event.key == pygame.K_4:
                mode = 'rect'

        if event.type == pygame.MOUSEBUTTONDOWN: #проверка на нажития мыши
            if event.button == 1: #лкм
                start_pos = event.pos #стартовая позиция получает текущую
                if mode in ['circle', 'rect']:
                    temp_surface = screen.copy() #копирование экрана (что бы фигуры не дублировались а просто предварительно отображались)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and start_pos:
                end_pos = event.pos
                if mode == 'circle': 
                    center = ((start_pos[0] + end_pos[0]) // 2, (start_pos[1] + end_pos[1]) // 2)
                    radius_circle = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5 / 2)
                    pygame.draw.circle(screen, current_color, center, radius_circle, 2)
                elif mode == 'rect':
                    rect = pygame.Rect(start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
                    pygame.draw.rect(screen, current_color, rect, 2)
                start_pos = None

        if event.type == pygame.MOUSEMOTION:
            if event.buttons[0] and mode in ['draw', 'erase']:
                if last_pos:
                    drawLineBetween(screen, last_pos, event.pos, radius, WHITE if mode == 'erase' else current_color)
                last_pos = event.pos
            else:
                last_pos = None

            if event.buttons[0] and mode in ['circle', 'rect'] and start_pos:
                screen.blit(temp_surface, (0, 0)) #отображение фигуры
                end_pos = event.pos
                if mode == 'circle':
                    center = ((start_pos[0] + end_pos[0]) // 2, (start_pos[1] + end_pos[1]) // 2)
                    radius_circle = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5 / 2)
                    pygame.draw.circle(screen, current_color, center, radius_circle, 2)
                elif mode == 'rect':
                    rect = pygame.Rect(start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
                    pygame.draw.rect(screen, current_color, rect, 2)

    pygame.display.flip() #обновления экрана
    clock.tick(60) #60 фпс

pygame.quit()
sys.exit()
