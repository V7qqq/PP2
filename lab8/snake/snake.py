#импортирую библиотеки что бы я мог написать змейку
import pygame # сам пайгейм
import sys # для выхода с приложения
import random # рандом библиотека

pygame.init() # импортирую методы с пайгейм что бы можно было пользоваться ими

WIDTH, HEIGHT = 1000, 1000 #Ширина и Высота основного экрана
CELL_SIZE = 20 # делим на количество клеточек 50x50 (1000/20 = 50)
GRID_WIDTH = WIDTH // CELL_SIZE #клетка 50
GRID_HEIGHT = HEIGHT // CELL_SIZE #клетка 50

screen = pygame.display.set_mode((WIDTH, HEIGHT)) #экран 1000 на 1000
clock = pygame.time.Clock() #подсчет фрейма
pygame.display.set_caption("Snakeeey 🐍") # название приложения

#Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

snake = [(10, 10), (20,20)]  #стартовая позиция змейки в клетках (змейка c двумя частями)
direction = (1, 0)  #идёт вправо
Speed = 10 #скорость
level_counter = 1 #отображалка левела
level_ready = 0 # готовность левела смены (4 левел_реди = +1 левел каунтер)
score_counter = 0 #подсчет очков


apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)) #координаты яблока (рандомные)


while True:
    screen.fill(WHITE) #экран белый

    #стандартный цикл проверки выхода из игры
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # управление стрелками
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1): #не дает змейки уйти (в себя (когда она идет вверх, она не может пойти резко вниз))
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1): #все остальное по той же логике
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)

   
    head_x, head_y = snake[0] # берём координаты головы
    dx, dy = direction # берём направление
    new_head = (head_x + dx, head_y + dy) #формируем новую голову
    snake.insert(0, new_head) #вставляем в начало массива

    if new_head == apple: #если яблоко съедено
        while True: # проверка что яблоко не спавнится внутри змейки
            apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if apple not in snake:
                break
        level_ready +=1 #+1 до 4
        score_counter +=1 # +1 к 000
    else:
        snake.pop()  # #либо удаляем хвост

    if level_ready == 4: #проверка на повышения левела
        level_ready = 0 #сбрасываем счетчик
        level_counter +=1 #повышаем лвл
        Speed += 5 #повышаем скорость змейки
        pygame.display.update()

    if (new_head in snake[1:] or  # проверка на самосъедание
        new_head[0] < 0 or new_head[0] >= GRID_WIDTH or 
        new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):

        screen.blit(text_1, (WIDTH// 2 - text_1.get_width() // 2, HEIGHT //2)) #game over надпись

        pygame.display.update()

        pygame.time.delay(3000) 
        pygame.quit()
        sys.exit()


    for block in snake:
        x, y = block
        pygame.draw.rect(screen, GREEN, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)) #рисуем змейку через цикл который вытаскивает x,y с блоков (координат : [(x1 координата,y1 координата), (и так далее)])

        pygame.draw.rect(screen, RED, (apple[0] * CELL_SIZE, apple[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)) #отрисовываем яблочко

        
    
    #размер шрифтов и их стиль (у нас none - стандартный)
    font_title_1 = pygame.font.Font(None, 100)
    font_title_2 = pygame.font.Font(None, 40)
    font_title_3 = pygame.font.Font(None, 60)

    text_1 = font_title_1.render(f"GAME OVER!", True, RED) #текст гейм овер
    text_2 = font_title_2.render(f"Score: {score_counter:03}", True, (0,0,0)) #текст score_counter (отформатированный под 000)
    text_3 = font_title_3.render(f"level : {level_counter}", True, (0,0,0)) # текст level_counter

    screen.blit(text_3, (WIDTH // 2 -  text_3.get_width() // 2, 50)) #левел каунтер отображение

    screen.blit(text_2, (30,60)) #скор каунтер отображение
    

    pygame.display.update()
    clock.tick(Speed)  #скорость змейки регулируя фреймы (чем больше кадров - тем быстрее змейка двигается. Потому что за 1 секунду обрабатывается больше фреймов)
