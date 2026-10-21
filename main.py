import random
import sys
import pygame

pygame.init()

# 1. NASTAVENÍ OKNA A HODIN
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Evader")
clock = pygame.time.Clock()

# 2. PROMĚNNÉ HRÁČE
player_x = 375
player_y = 500
player_size = 50
player_speed = 5

# 3. METEORITY
meteor_size = 40
meteor_speed = 4
num_meteors = 4

# 4. LASERY
lasers = []
laser_speed = 10
laser_width = 5
laser_height = 15

# 5. NAČTENÍ OBRÁZKŮ
player_img = pygame.image.load("player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (player_size, player_size))

meteor_img = pygame.image.load("meteor.png").convert_alpha()
meteor_img = pygame.transform.scale(meteor_img, (meteor_size, meteor_size))

life_img = pygame.image.load("life.png").convert_alpha()
life_img = pygame.transform.scale(life_img, (25, 25))

default_background = pygame.image.load("default_background.jpg").convert()
bg_img = pygame.transform.scale(default_background, (WIDTH, HEIGHT))

# 6. POZADÍ A PÍSMA
bg_y = 0
bg_speed = 2

font = pygame.font.SysFont("Arial", 30)
title_font = pygame.font.SysFont("Arial", 50, bold=True)

# 7. NAČTENÍ NEJVYŠŠÍHO SKÓRE
score = 0
try:
    with open("highscore.txt", "r") as file:
        highscore = int(file.read())
except (FileNotFoundError, ValueError):
    highscore = 0

lives = 3
game_state = "MENU"  # Stavy hry: "MENU", "PLAYING", "GAME_OVER"

meteors = []


def reset_game():
    """Funkce pro resetování všech herních hodnot před novou hrou."""
    global player_x, player_y, meteor_speed, score, lives, lasers, meteors
    player_x = 375
    player_y = 500
    meteor_speed = 4
    score = 0
    lives = 3
    lasers = []

    meteors = []
    for i in range(num_meteors):
        x = random.randint(0, WIDTH - meteor_size)
        y = random.randint(-500, -meteor_size)
        meteors.append(pygame.Rect(x, y, meteor_size, meteor_size))


# 8. HLAVNÍ SMYČKA
running = True
while running:
    # --- A) ODCHYTÁVÁNÍ UDÁLOSTÍ ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # V MENU
            if game_state == "MENU":
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    reset_game()
                    game_state = "PLAYING"

            # V HŘE
            elif game_state == "PLAYING":
                if event.key == pygame.K_SPACE:
                    laser_x = (
                        player_x + (player_size // 2) - (laser_width // 2)
                    )
                    laser_y = player_y
                    lasers.append(
                        pygame.Rect(
                            laser_x, laser_y, laser_width, laser_height
                        )
                    )

            # V GAME OVER
            elif game_state == "GAME_OVER":
                if event.key == pygame.K_r:
                    reset_game()
                    game_state = "PLAYING"
                elif event.key == pygame.K_m:
                    game_state = "MENU"

    # --- B) LOGIKA HRY (Pouze když se hraje) ---
    # Posun pozadí běží neustále pro hezký vizuální efekt
    bg_y += bg_speed
    if bg_y >= HEIGHT:
        bg_y = 0

    if game_state == "PLAYING":
        # Ovládání (WASD + Šipky)
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 0:
            player_x -= player_speed
        if (
            keys[pygame.K_RIGHT] or keys[pygame.K_d]
        ) and player_x < WIDTH - player_size:
            player_x += player_speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_y > 0:
            player_y -= player_speed
        if (
            keys[pygame.K_DOWN] or keys[pygame.K_s]
        ) and player_y < HEIGHT - player_size:
            player_y += player_speed

        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

        # Kontrola a zápis rekordu
        if score > highscore:
            highscore = score
            with open("highscore.txt", "w") as file:
                file.write(str(highscore))

        # Pohyb meteoritů a kolize s hráčem
        for meteor in meteors:
            meteor.y += meteor_speed

            if meteor.y > HEIGHT:
                meteor.y = -meteor_size
                meteor.x = random.randint(0, WIDTH - meteor_size)

            if player_rect.colliderect(meteor):
                lives -= 1
                meteor.y = -meteor_size
                meteor.x = random.randint(0, WIDTH - meteor_size)

                if lives <= 0:
                    game_state = "GAME_OVER"

        # Pohyb laserů nahoru
        for laser in lasers[:]:
            laser.y -= laser_speed
            if laser.y < -laser_height:
                lasers.remove(laser)

        # Kontrola zásahu meteoritu laserem
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

    # --- C) VYKRESLOVÁNÍ ---
    # 1. Pohybující se pozadí kreslíme vždy
    screen.blit(bg_img, (0, bg_y))
    screen.blit(bg_img, (0, bg_y - HEIGHT))

    # 2. Vykreslení podle stavu
    if game_state == "MENU":
        title_text = title_font.render("SPACE EVADER", True, (0, 255, 255))
        start_text = font.render(
            "Press SPACE or ENTER to Start", True, (255, 255, 255)
        )
        high_score_text = font.render(
            f"High Score: {highscore}", True, (255, 215, 0)
        )

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 180))
        screen.blit(
            start_text, (WIDTH // 2 - start_text.get_width() // 2, 300)
        )
        screen.blit(
            high_score_text,
            (WIDTH // 2 - high_score_text.get_width() // 2, 380),
        )

    elif game_state == "PLAYING":
        screen.blit(player_img, (player_x, player_y))

        for meteor in meteors:
            screen.blit(meteor_img, meteor)

        for laser in lasers:
            pygame.draw.rect(screen, (0, 255, 255), laser)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        high_score_text = font.render(
            f"High Score: {highscore}", True, (255, 215, 0)
        )

        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 45))

        for i in range(lives):
            screen.blit(life_img, (WIDTH - 35 - (i * 30), 15))

    elif game_state == "GAME_OVER":
        game_over_text = title_font.render("GAME OVER", True, (255, 50, 50))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        high_score_text = font.render(
            f"High Score: {highscore}", True, (255, 215, 0)
        )
        restart_text = font.render(
            "Press 'R' to Restart | 'M' for Menu", True, (200, 200, 200)
        )

        screen.blit(
            game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 150)
        )
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 240))
        screen.blit(
            high_score_text,
            (WIDTH // 2 - high_score_text.get_width() // 2, 280),
        )
        screen.blit(
            restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 360)
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
