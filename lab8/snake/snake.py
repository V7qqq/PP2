import pygame
import sys
import random
import psycopg2

def connect_to_database_and_add_user(username): # Функция для подключения к базе данных и добавления пользователя
    conn = psycopg2.connect( #подключение к базе данных
        dbname="snake", #название базы данных
        user="rrovi1", #имя пользователя
        password="15Rodionmagic", #пароль
        host="38.244.137.21", #хост
        port="5432" #порт
    )
    cur = conn.cursor() #создаем курсор

    cur.execute("SELECT id FROM users WHERE username = %s", (username,)) #поиск пользователя по имени
    user = cur.fetchone() #получаем пользователя
    if user: #если пользователь найден
        user_id = user[0] #получаем id пользователя
    else: #если пользователь не найден
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,)) #вставляем пользователя в таблицу
        user_id = cur.fetchone()[0] #получаем id пользователя
        conn.commit() #коммитим изменения

    cur.execute("SELECT score, level FROM user_scores WHERE user_id = %s", (user_id,)) #получаем счет и уровень пользователя
    score_data = cur.fetchone() #получаем данные о счете
    if not score_data: #если данные о счете не найдены
        cur.execute("INSERT INTO user_scores (user_id) VALUES (%s)", (user_id,)) #вставляем данные о счете
        conn.commit() #коммитим изменения
        score = 0 #начальный счет
        level = 1 #начальный уровень
    else:
        score, level = score_data #получаем счет и уровень пользователя

    cur.close() #закрываем курсор
    conn.close() # закрываем соединение с базой данных
    return user_id, score, level #возвращаем id пользователя, счет и уровень

def save_game_state(user_id, score, level): # Функция для сохранения состояния игры в базе данных
    conn = psycopg2.connect( #подключение к базе данных
        dbname="snake", #название базы данных
        user="rrovi1", #имя пользователя
        password="15Rodionmagic", #пароль
        host="38.244.137.21", #хост
        port="5432" #порт
    )
    cur = conn.cursor() 
    cur.execute( #обновление данных о счете и уровне
        "UPDATE user_scores SET score = %s, level = %s WHERE user_id = %s",
        (score, level, user_id)
    )
    conn.commit()
    cur.close() #закрываем курсор
    conn.close()

username = input("Enter your username: ") #вводим имя пользователя
user_id, score_counter, level_counter = connect_to_database_and_add_user(username) #подключаемся к базе данных и добавляем пользователя
Speed = 10 + (level_counter - 1) * 5 #начальная скорость

pygame.init() #инициализация pygame

WIDTH, HEIGHT = 1000, 1000 #размер окна
CELL_SIZE = 20 #размер клетки
GRID_WIDTH = WIDTH // CELL_SIZE #количество клеток по ширине
GRID_HEIGHT = HEIGHT // CELL_SIZE #количество клеток по высоте

screen = pygame.display.set_mode((WIDTH, HEIGHT)) #создаем окно
clock = pygame.time.Clock() #создаем часы что бы работать с фпс
pygame.display.set_caption("Snakeeey") #название окна

# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

snake = [(10, 10), (20, 20)] #начальная позиция змейки (2 клетки)
direction = (1, 0) ##начальное направление змейки (вправо)
level_ready = 0 #счетчик уровня
value = 1 #значение для увеличения счета
apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)) #начальная позиция яблока

while True: #цикл игры
    screen.fill(WHITE) #заполняем экран белым цветом

    for event in pygame.event.get(): ##обработка событий
        if event.type == pygame.QUIT: #выход из игры
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN: #обработка нажатий клавиш
            if event.key == pygame.K_UP and direction != (0, 1): ##вверх
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1): ##вниз
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0): #влево
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0): #вправо
                direction = (1, 0)
            elif event.key == pygame.K_ESCAPE: #пауза
                save_game_state(user_id, score_counter, level_counter) #сохраняем состояние пользователя
                pause = True #создаем булевую функцию связанную с паузой
                pause_font = pygame.font.Font(None, 60) #шрифт для паузы
                pause_text = pause_font.render("PAUSED : Press 'ESC' to resume", True, RED) #текст паузы
                screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2)) #отображаем текст паузы
                pygame.display.update() #обновляем экран
                while pause:
                    for pause_event in pygame.event.get(): #обработка событий паузы
                        if pause_event.type == pygame.QUIT: #выход из игры
                            pygame.quit()
                            sys.exit()
                        elif pause_event.type == pygame.KEYDOWN and pause_event.key == pygame.K_ESCAPE: #выход из паузы
                            pause = False


    head_x, head_y = snake[0] #получаем координаты головы змейки
    dx, dy = direction #получаем направление движения змейки
    new_head = (head_x + dx, head_y + dy) #получаем новые координаты головы змейки
    snake.insert(0, new_head) #добавляем новые координаты головы в начало списка змейки

    if new_head == apple: #если змейка съела яблоко
        while True: #генерируем новые координаты яблока
            apple = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)) #новые координаты яблока
            if apple not in snake: #если яблоко не попало на змейку
                break #выходим из цикла
        score_counter += value #увеличиваем счет
        level_ready += 1 #увеличиваем счетчик уровня
    else:
        snake.pop() #удаляем последний элемент змейки

    if level_ready == 4: #если счетчик уровня равен 4
        level_ready = 0 #обнуляем счетчик уровня
        level_counter += 1 #увеличиваем уровень
        Speed += 5 #увеличиваем скорость

    if (new_head in snake[1:] or new_head[0] < 0 or new_head[0] >= GRID_WIDTH or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):  #если змейка врезалась в себя или в стену
        font_title_1 = pygame.font.Font(None, 100) #шрифт для текста
        text_1 = font_title_1.render("GAME OVER!", True, RED) #текст окончания игры
        screen.blit(text_1, (WIDTH // 2 - text_1.get_width() // 2, HEIGHT // 2)) #отображаем текст окончания игры
        pygame.display.update() #обновляем экран
        score_counter = 0 #обнуляем счет
        level_counter = 1 #обнуляем уровень
        save_game_state(user_id, score_counter, level_counter) #сохраняем состояние пользователя
        pygame.time.delay(3000) #ждем 3 секунды
        pygame.quit() #выход из игры
        sys.exit()

    for block in snake: #отрисовка змейки
        x, y = block #получаем координаты блока
        pygame.draw.rect(screen, GREEN, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)) #отрисовка блока

    
    pygame.draw.rect(screen, RED, (apple[0] * CELL_SIZE, apple[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)) #рисуем яблочко

    font_title_2 = pygame.font.Font(None, 40) #шрифт для текста score
    font_title_3 = pygame.font.Font(None, 60) #шрифт для текста level
    text_2 = font_title_2.render(f"Score: {score_counter:03}", True, BLACK) #рендерим их
    text_3 = font_title_3.render(f"Level: {level_counter}", True, BLACK)
    screen.blit(text_2, (30, 60)) #отображаем текст счета
    screen.blit(text_3, (WIDTH // 2 - text_3.get_width() // 2, 50)) #отображаем текст уровня

    pygame.display.update() #обновляем экран
    clock.tick(Speed) #ограничиваем скорость игры (фпсом)
