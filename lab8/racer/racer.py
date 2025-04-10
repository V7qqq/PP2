#импортируем библиотеки
import pygame
import sys
import random


# достаем методы
pygame.init()
pygame.mixer.init()

# настройка экрана и фпс
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60
FramePerSec = pygame.time.Clock()

#цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

#экран
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")
road = pygame.image.load("tutorial/AnimatedStreet.png")

# шрифт
font = pygame.font.SysFont(None, 60)
font_title = pygame.font.Font(None, 40)

# счетчики
score_counter = 0
coin_counter = 0
coin_level = 0

coin_visible = False #проверка на видимости коина
coin_spawn_delay = random.randint(120, 240)  #делей на спавн от 2 до 4 секунд
coin_timer = 0 #тут он по фреймам будет плюсоваться и уже сравнмваться с coin_spawn_delay

crash = pygame.mixer.Sound("tutorial/crash.wav")
background = pygame.mixer.Sound("tutorial/background.wav")

# класс врага
class Enemy(pygame.sprite.Sprite): #наследуем с класса спрайт
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("tutorial/Enemy.png") #берем картинку
        self.rect = self.image.get_rect() #формируем хитбокс что бы была коллизия
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, 10)
        if self.rect.top > SCREEN_HEIGHT: #если машина проехала
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)
            global score_counter #вызываем глобальную переменную
            score_counter += 1 #добавляем очко

    def draw(self, surface):
        surface.blit(self.image, self.rect) #рисуем машину

# класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("tutorial/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520) #спавнимся в центре

    def update(self):
        pressed_keys = pygame.key.get_pressed() #движение
        if self.rect.left > 0 and pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)

    def draw(self, surface): #рисуем игрока
        surface.blit(self.image, self.rect)

# Класс монеты
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("tutorial/coin.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.reset_position()
        self.value = random.randint(1, 10) #рандомная стоимость монетки от 1 до 10

    def reset_position(self): 
        while True:
            x = random.randint(40, SCREEN_WIDTH - 40)
            y = 0
            self.rect.center = (x, y)
            if not self.rect.colliderect(E1.rect):
                break
            self.value = random.randint(1, 10)


    def move(self):
        self.rect.move_ip(0, 10)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()
            global coin_visible
            coin_visible = False
            

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        font = pygame.font.SysFont(None, 24)
        value_text = font.render(str(self.value), True, BLACK)
        text_rect = value_text.get_rect(center=self.rect.center)
        surface.blit(value_text, text_rect)

# создаем объекты
P1 = Player()
E1 = Enemy()
C1 = Coin()

background.play(-1)

enemies = pygame.sprite.Group() #формируем группу енемис из класса спрайта
enemies.add(E1) #добавляем туда енеми машину
all_sprites = pygame.sprite.Group() #формируем группу спрайтов и вставляем туда плеера и енеми для одновременного например обновления
all_sprites.add(P1)
all_sprites.add(E1)

# цикл
running = True
while running: 
    DISPLAYSURF.blit(road, (0,0)) #вставляем картинку на фон

    for event in pygame.event.get(): #проверка на выход
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    # обновление состояний
    all_sprites.update() 
    E1.move()
    C1.move()
    # монетка появляется через рандомное время
    if not coin_visible:
        coin_timer += 1
        if coin_timer >= coin_spawn_delay: #проверка на больше или равно (так как фрейм на койн таймере может быть не четным и тогда if не сработает уже никогда)
            coin_visible = True
            coin_timer = 0
            coin_spawn_delay = random.randint(120, 240)
            C1.reset_position()


    # проверка сбора монеты
    if coin_visible and pygame.sprite.collide_rect(P1, C1):
        coin_counter += 1
        coin_level += C1.value
        coin_visible = False  # монетка исчезает после сбора
    
    
    if coin_level >= 5: #каждая 5 монетка добавляет +10 фпс усложняя игру
        FPS += 10
        coin_level = 0
    

    # проверка столкновения с врагом
    if pygame.sprite.collide_rect(P1, E1):
        crash.play() #звук
        background.stop()
        while pygame.mixer.get_busy():
            pygame.time.delay(100)

        game_over_text = font.render("Game Over!", True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        DISPLAYSURF.blit(game_over_text, text_rect)
        pygame.display.update()
        pygame.time.delay(3000)
        pygame.quit()
        sys.exit()

    # отрисовка объектов
    P1.draw(DISPLAYSURF)
    E1.draw(DISPLAYSURF)
    if coin_visible:
        C1.draw(DISPLAYSURF)


    # отображение счёта
    score_text = font_title.render(f"Score: {score_counter:03}", True, BLACK)
    coin_text = font_title.render(f"Coins: {coin_counter:02}", True, BLACK)
    DISPLAYSURF.blit(score_text, (20, 20))
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - coin_text.get_width() - 20, 20))

    # обновление экрана
    pygame.display.update()
    FramePerSec.tick(FPS)
