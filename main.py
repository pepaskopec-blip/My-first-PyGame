import sys

import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("PyGame")

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    screen.fill((0,255,0))
    pygame.draw.rect(screen, (255, 0, 0), (375, 500, 50, 50))
    pygame.display.flip()
    clock.tick(60)



