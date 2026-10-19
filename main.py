import random
import sys
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My first PyGame")

clock = pygame.time.Clock()

player_x = 375
player_y = 500
player_size = 50
player_speed = 5

meteor_size = 40
meteor_x = random.randint(0, WIDTH - meteor_size)
meteor_y = -meteor_size
meteor_speed = 4

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed

    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - player_size:
        player_y += player_speed

    meteor_y += meteor_speed

    if meteor_y > HEIGHT:
        meteor_y = -meteor_size
        meteor_x = random.randint(
            0, WIDTH - meteor_size
        )

    screen.fill((20,40,40))

    pygame.draw.rect(
        screen, (255, 50, 50), (player_x, player_y, player_size, player_size)
    )

    pygame.draw.rect(
        screen, (255, 200, 0), (meteor_x, meteor_y, meteor_size, meteor_size)
    )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()



