import pygame
import sys
pygame.init()

WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("big balls")
x,y = 500,500
speed = 20
while True:
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x - 15 > 15:
        x -= speed
    if keys[pygame.K_RIGHT] and x + 15 < WIDTH-15:
        x += speed
    if keys[pygame.K_UP] and y - 15 > 15:
        y -= speed
    if keys[pygame.K_DOWN] and y + 15 < HEIGHT-15:
        y += speed

    pygame.draw.circle(screen, (0,0,0),(x,y),15)



    pygame.display.flip()
    clock.tick(60)