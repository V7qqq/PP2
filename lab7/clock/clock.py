import pygame
import datetime
import math
import sys
import os

pygame.init()
x_bg,y_bg = 1000,1000
screen = pygame.display.set_mode((x_bg, y_bg), pygame.RESIZABLE)
clock = pygame.time.Clock()
image = pygame.image.load("clock/mickeyclock.jpeg").convert_alpha()

x = x_bg // 2 + 200
y = y_bg // 2 + 25

minute_arrow = 200
second_arrow = 300

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    now = datetime.datetime.now()
    minute = now.minute
    second = now.second
    screen.fill((255,255,255))
    screen.blit(image, (0,0))

    angle_minute = math.radians(6 * minute - 90)
    angle_second = math.radians(6 * second - 90)
    minute_x = x + minute_arrow * math.cos(angle_minute)
    minute_y = y + minute_arrow * math.sin(angle_minute)

    second_x = x + second_arrow * math.cos(angle_second)
    second_y = y + second_arrow * math.sin(angle_second)

    pygame.draw.line(screen, (0, 0, 255), (x, y), (minute_x, minute_y), 8)
    pygame.draw.line(screen, (255, 0, 0), (x, y), (second_x, second_y), 5)










    pygame.display.flip()

    
    clock.tick(60)