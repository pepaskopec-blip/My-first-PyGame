import random
import sys
import pygame

pygame.init()

# 1. Window settings and clock
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Evader")
clock = pygame.time.Clock()

# 2. player variables
player_x = 375
player_y = 500
player_size = 50
player_speed = 5

# 3. METEORITES
meteor_size = 40
meteor_speed = 4
num_meteors = 4

# 4. ENEMY SPACESHIP
enemy_size = 50
enemy_x = WIDTH // 2 - enemy_size // 2
enemy_y = 60
enemy_speed_x = 3
enemy_alive = True
enemy_respawn_timer = 0

# 5. LASERS
lasers = []
laser_speed = 10
laser_width = 5
laser_height = 15

# Enemy lasers
enemy_lasers = []
enemy_laser_speed = 7
enemy_shoot_timer = 0

# power-ups
powerups = []
powerup_speed = 3

# particles
particles = []

# 6. image load
player_img = pygame.image.load("player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (player_size, player_size))

meteor_img = pygame.image.load("meteor.png").convert_alpha()
meteor_img = pygame.transform.scale(meteor_img, (meteor_size, meteor_size))

life_img = pygame.image.load("life.png").convert_alpha()
life_img = pygame.transform.scale(life_img, (25, 25))

coin_img = pygame.image.load("coin.png").convert_alpha()
coin_img = pygame.transform.scale(coin_img, (25, 25))

default_background = pygame.image.load("default_background.jpg").convert()
bg_img = pygame.transform.scale(default_background, (WIDTH, HEIGHT))

enemy_spaceship_img = pygame.image.load("enemy_spaceship.png").convert_alpha()
enemy_spaceship_img = pygame.transform.scale(
    enemy_spaceship_img, (enemy_size, enemy_size)
)

# 7. background and fonts
bg_y = 0
bg_speed = 2

font = pygame.font.SysFont("Arial", 30)
title_font = pygame.font.SysFont("Arial", 50, bold=True)

# 8. high score
score = 0
try:
    with open("highscore.txt", "r") as file:
        highscore = int(file.read())
except (FileNotFoundError, ValueError):
    highscore = 0

# coins
coins = 0
try:
    with open("coins.txt", "r") as file:
        coins = int(file.read())
except (FileNotFoundError, ValueError):
    coins = 0

lives = 3
game_state = "MENU"
meteors = []


def save_highscore(val):
    with open("highscore.txt", "w") as file:
        file.write(str(val))


def save_coins(val):
    with open("coins.txt", "w") as file:
        file.write(str(val))


def create_explosion(x, y, color=(255, 165, 0)):
    for _ in range(15):
        particles.append(
            {
                "x": x,
                "y": y,
                "vx": random.uniform(-4, 4),
                "vy": random.uniform(-4, 4),
                "radius": random.randint(3, 6),
                "color": color,
                "lifetime": random.randint(15, 25),
            }
        )


def draw_coins(x, y, center=False):
    """Vykreslí ikonku coinu a vedle ní počet coinů."""
    text = font.render(str(coins), True, (255, 215, 0))
    total_width = coin_img.get_width() + 8 + text.get_width()
    if center:
        x = x - total_width // 2
    icon_y = y + (text.get_height() - coin_img.get_height()) // 2
    screen.blit(coin_img, (x, icon_y))
    screen.blit(text, (x + coin_img.get_width() + 8, y))


def reset_game():
    global player_x, player_y, meteor_speed, score, lives, lasers, enemy_lasers, meteors
    global enemy_x, enemy_alive, enemy_respawn_timer, enemy_shoot_timer, powerups
    global particles

    player_x = 375
    player_y = 500
    enemy_x = WIDTH // 2 - enemy_size // 2
    enemy_alive = True
    enemy_respawn_timer = 0
    enemy_shoot_timer = 0

    meteor_speed = 4
    score = 0
    lives = 3
    lasers = []
    enemy_lasers = []
    powerups = []
    particles = []

    meteors = []
    for i in range(num_meteors):
        x = random.randint(0, WIDTH - meteor_size)
        y = random.randint(-500, -meteor_size)
        meteors.append(pygame.Rect(x, y, meteor_size, meteor_size))


# 9. main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_state == "MENU":
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    reset_game()
                    game_state = "PLAYING"

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

            elif game_state == "GAME_OVER":
                if event.key == pygame.K_r:
                    reset_game()
                    game_state = "PLAYING"
                elif event.key == pygame.K_m:
                    game_state = "MENU"

    # --- GAME LOGIC ---
    bg_y += bg_speed
    if bg_y >= HEIGHT:
        bg_y = 0

    for p in particles[:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["radius"] -= 0.2
        p["lifetime"] -= 1
        if p["lifetime"] <= 0 or p["radius"] <= 0:
            particles.remove(p)

    if game_state == "PLAYING":
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

        if score > highscore:
            highscore = score

        # Power-ups
        for p_up in powerups[:]:
            p_up.y += powerup_speed
            if p_up.y > HEIGHT:
                powerups.remove(p_up)
            elif player_rect.colliderect(p_up):
                if lives < 5:
                    lives += 1
                powerups.remove(p_up)

        # Enemy
        if enemy_alive:
            enemy_x += enemy_speed_x
            if enemy_x <= 0 or enemy_x >= WIDTH - enemy_size:
                enemy_speed_x *= -1

            enemy_shoot_timer += 1
            if enemy_shoot_timer >= 60:
                enemy_shoot_timer = 0
                e_laser_x = enemy_x + (enemy_size // 2) - 2
                enemy_lasers.append(
                    pygame.Rect(e_laser_x, enemy_y + enemy_size, 5, 15)
                )
        else:
            enemy_respawn_timer -= 1
            if enemy_respawn_timer <= 0:
                enemy_x = random.randint(0, WIDTH - enemy_size)
                enemy_alive = True

        # Enemy lasers
        for e_laser in enemy_lasers[:]:
            e_laser.y += enemy_laser_speed
            if e_laser.y > HEIGHT:
                enemy_lasers.remove(e_laser)
            elif player_rect.colliderect(e_laser):
                lives -= 1
                enemy_lasers.remove(e_laser)
                create_explosion(
                    player_x + player_size // 2,
                    player_y + player_size // 2,
                    (255, 0, 0),
                )
                if lives <= 0:
                    game_state = "GAME_OVER"
                    save_highscore(highscore)
                    save_coins(coins)

        # Meteors
        for meteor in meteors:
            meteor.y += meteor_speed

            if meteor.y > HEIGHT:
                meteor.y = -meteor_size
                meteor.x = random.randint(0, WIDTH - meteor_size)

            if player_rect.colliderect(meteor):
                lives -= 1
                create_explosion(
                    player_x + player_size // 2,
                    player_y + player_size // 2,
                    (255, 0, 0),
                )
                meteor.y = -meteor_size
                meteor.x = random.randint(0, WIDTH - meteor_size)

                if lives <= 0:
                    game_state = "GAME_OVER"
                    save_highscore(highscore)
                    save_coins(coins)

        # Player lasers
        for laser in lasers[:]:
            laser.y -= laser_speed
            if laser.y < -laser_height:
                lasers.remove(laser)
                continue

            # Enemy hit
            if enemy_alive:
                enemy_rect = pygame.Rect(
                    enemy_x, enemy_y, enemy_size, enemy_size
                )
                if laser.colliderect(enemy_rect):
                    score += 5
                    coins += 3
                    enemy_alive = False
                    enemy_respawn_timer = 180
                    create_explosion(
                        enemy_x + enemy_size // 2,
                        enemy_y + enemy_size // 2,
                        (255, 50, 50),
                    )

                    if random.random() < 0.5:
                        powerups.append(
                            pygame.Rect(enemy_x + 12, enemy_y, 25, 25)
                        )

                    lasers.remove(laser)
                    continue

            # Meteor hit
            for meteor in meteors:
                if laser.colliderect(meteor):
                    score += 1
                    coins += 1
                    meteor_speed += 0.05
                    create_explosion(
                        meteor.x + meteor_size // 2,
                        meteor.y + meteor_size // 2,
                        (255, 165, 0),
                    )
                    meteor.y = -meteor_size
                    meteor.x = random.randint(0, WIDTH - meteor_size)
                    if laser in lasers:
                        lasers.remove(laser)
                    break

    # --- RENDERING ---
    screen.blit(bg_img, (0, bg_y))
    screen.blit(bg_img, (0, bg_y - HEIGHT))

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
        draw_coins(WIDTH // 2, 460, center=True)

    elif game_state == "PLAYING":
        screen.blit(player_img, (player_x, player_y))

        for meteor in meteors:
            screen.blit(meteor_img, meteor)

        if enemy_alive:
            screen.blit(enemy_spaceship_img, (enemy_x, enemy_y))

        for e_laser in enemy_lasers:
            pygame.draw.rect(screen, (255, 50, 50), e_laser)

        for laser in lasers:
            pygame.draw.rect(screen, (0, 255, 255), laser)

        for p_up in powerups:
            screen.blit(life_img, p_up)

        for p in particles:
            pygame.draw.circle(
                screen, p["color"], (int(p["x"]), int(p["y"])), int(p["radius"])
            )

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        high_score_text = font.render(
            f"High Score: {highscore}", True, (255, 215, 0)
        )

        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 45))
        draw_coins(10, 80)

        for i in range(lives):
            screen.blit(life_img, (WIDTH - 35 - (i * 30), 15))

    elif game_state == "GAME_OVER":
        for p in particles:
            pygame.draw.circle(
                screen, p["color"], (int(p["x"]), int(p["y"])), int(p["radius"])
            )

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
        draw_coins(WIDTH // 2, 320, center=True)
        screen.blit(
            restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 380)
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()