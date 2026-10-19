import random
import sys
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My first PyGame")

clock = pygame.time.Clock()

# Hráč
player_x = 375
player_y = 500
player_size = 50
player_speed = 5

# Meteority (seznam)
meteor_size = 40
meteor_speed = 4
num_meteors = 4

# Lasery
lasers = []
laser_speed = 10
laser_width = 5
laser_height = 15

#Načtení a změna velikosti obrázků hráče
player_img = pygame.image.load("player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (player_size, player_size))

meteor_img = pygame.image.load("meteor.png").convert_alpha()
meteor_img = pygame.transform.scale(meteor_img, (meteor_size, meteor_size))

life_icon = pygame.transform.scale(player_img, (25, 25))

meteors = []
for i in range(num_meteors):
    x = random.randint(0, WIDTH - meteor_size)
    y = random.randint(-500, -meteor_size)  # Začínají v různé výšce nad okny
    meteors.append(pygame.Rect(x, y, meteor_size, meteor_size))

score = 0
game_over = False

lives = 3

font = pygame.font.SysFont("Arial", 30)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                player_x = 375
                player_y = 500
                meteor_speed = 4
                score = 0
                lasers = []

        if event.type == pygame.KEYDOWN:
            #Střílení mezerníkem
            if event.key == pygame.K_SPACE and not game_over:
                laser_x = player_x + (player_size // 2) - (laser_width // 2)
                laser_y = player_y
                lasers.append(
                    pygame.Rect(laser_x, laser_y, laser_width, laser_height)
                )

                # Obnovení meteoritů nad obrazovku
                meteors = []
                for i in range(num_meteors):
                    x = random.randint(0, WIDTH - meteor_size)
                    y = random.randint(-500, -meteor_size)
                    meteors.append(pygame.Rect(x, y, meteor_size, meteor_size))

                game_over = False

    if not game_over:
        # Ovládání (WASD + šipky)
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 0:
            player_x -= player_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < WIDTH - player_size:
            player_x += player_speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_y > 0:
            player_y -= player_speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_y < HEIGHT - player_size:
            player_y += player_speed

        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

        # Pohyb a kolize pro VŠECHNY meteority ze seznamu
        for meteor in meteors:
            meteor.y += meteor_speed

            # Reset meteoritu a přičtení skóre
            if meteor.y > HEIGHT:
                meteor.y = -meteor_size
                meteor.x = random.randint(0, WIDTH - meteor_size)
                score += 1
                meteor_speed += 0.1

            # Kolize s hráčem
            if player_rect.colliderect(meteor):
                lives -= 1
                meteor.y = -meteor_size
                meteor.x = random.randint(0, WIDTH - meteor_size)

                if lives <= 0:
                    game_over = True

            for laser in lasers[:]:
                laser.y -= laser_speed
                if laser.y < -laser_height:
                    lasers.remove(laser)

            for laser in lasers[:]:
                for meteor in meteors:
                    if laser.colliderect(meteor):
                        score += 1
                        meteor_speed += 0.05

                        meteor.y = -meteor_size
                        meteor.x = random.randint(0, WIDTH - meteor_size)

                        if laser in lasers:
                            lasers.remove(laser)
                            break

    # --- VYKRESLOVÁNÍ ---
    screen.fill((0, 0, 0))

    if not game_over:
        # 1. Kreslení obrázku hráče
        screen.blit(player_img, (player_x, player_y))

        # 2. Kreslení všech obrázků meteoritů
        for meteor in meteors:
            screen.blit(meteor_img, meteor)

        # 3. Kreslení skóre
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # 4. Kreslení ikonek životů
        for i in range (lives):
            screen.blit(life_icon, (WIDTH - 35 - (i * 30), 15))

        # 5. Kreslení laserů
        for laser in lasers:
            pygame.draw.rect(screen, (0, 255, 255), laser)
    else:
        game_over_text = font.render(
            f"GAME OVER! Score: {score}", True, (255, 50, 50)
        )
        screen.blit(game_over_text, (WIDTH // 2 - 140, HEIGHT // 2 - 40))

        game_over_text = font.render(
            f"Press 'R' to restart", True, (255, 50, 50)
        )
        screen.blit(game_over_text, (WIDTH // 2 - 115, HEIGHT // 2 - 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
