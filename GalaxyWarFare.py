import pygame
import random
import math

# =========================================
# INITIALIZE
# =========================================
pygame.init()

WIDTH, HEIGHT = 1200, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 GALAXY WARFARE")

clock = pygame.time.Clock()
FPS = 60

# =========================================
# COLORS
# =========================================
BLACK = (5, 5, 15)
WHITE = (255, 255, 255)
RED = (255, 70, 70)
GREEN = (0, 255, 100)
BLUE = (0, 180, 255)
YELLOW = (255, 255, 0)
PURPLE = (180, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 140, 0)

# =========================================
# FONTS
# =========================================
title_font = pygame.font.SysFont("Arial", 65, bold=True)
font = pygame.font.SysFont("Arial", 32, bold=True)
small_font = pygame.font.SysFont("Arial", 22)

# =========================================
# PLAYER SETTINGS
# =========================================
player_x = WIDTH // 2
player_y = HEIGHT - 120

player_speed = 8
player_health = 100
player_shield = 50

# =========================================
# GAME VARIABLES
# =========================================
bullets = []
enemy_bullets = []
enemies = []
particles = []
powerups = []
energy_boosters = []
stars = []

score = 0
coins = 0
level = 1

enemy_speed = 4
shoot_delay = 0

boss_mode = False
boss_health = 300

game_over = False
running = True

# =========================================
# STAR BACKGROUND
# =========================================
for i in range(200):

    stars.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.randint(1, 4)
    ])

# =========================================
# FUNCTIONS
# =========================================
def glow_text(text, font, color, x, y):

    glow = font.render(text, True, WHITE)
    screen.blit(glow, (x + 2, y + 2))

    txt = font.render(text, True, color)
    screen.blit(txt, (x, y))


def create_explosion(x, y, amount=30):

    for i in range(amount):

        particles.append([
            x,
            y,
            random.randint(-7, 7),
            random.randint(-7, 7),
            random.randint(3, 8)
        ])

# =========================================
# MAIN GAME LOOP
# =========================================
while running:

    clock.tick(FPS)

    # =====================================
    # BACKGROUND
    # =====================================
    screen.fill(BLACK)

    # Animated stars
    for star in stars:

        pygame.draw.circle(
            screen,
            WHITE,
            (star[0], star[1]),
            star[2]
        )

        star[1] += star[2]

        if star[1] > HEIGHT:
            star[0] = random.randint(0, WIDTH)
            star[1] = 0

    # =====================================
    # EVENTS
    # =====================================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # =====================================
    # CONTROLS
    # =====================================
    keys = pygame.key.get_pressed()

    if not game_over:

        if keys[pygame.K_LEFT] and player_x > 20:
            player_x -= player_speed

        if keys[pygame.K_RIGHT] and player_x < WIDTH - 90:
            player_x += player_speed

        if keys[pygame.K_UP] and player_y > 100:
            player_y -= player_speed

        if keys[pygame.K_DOWN] and player_y < HEIGHT - 100:
            player_y += player_speed

        # SHOOTING
        if keys[pygame.K_SPACE]:

            if shoot_delay == 0:

                bullets.append(
                    pygame.Rect(player_x + 32, player_y, 8, 25)
                )

                # Triple bullets after level 5
                if level >= 5:

                    bullets.append(
                        pygame.Rect(player_x + 12, player_y, 8, 25)
                    )

                    bullets.append(
                        pygame.Rect(player_x + 52, player_y, 8, 25)
                    )

                shoot_delay = 10

    if shoot_delay > 0:
        shoot_delay -= 1

    # =====================================
    # ENEMY SPAWN
    # =====================================
    if not boss_mode:

        if random.randint(1, 25) == 1:

            enemy = pygame.Rect(
                random.randint(50, WIDTH - 100),
                -80,
                70,
                70
            )

            enemies.append(enemy)

    # =====================================
    # ENERGY BOOSTER SPAWN
    # =====================================
    if random.randint(1, 400) == 1 and not game_over:

        booster = pygame.Rect(
            random.randint(50, WIDTH - 100),
            -50,
            40,
            40
        )

        energy_boosters.append(booster)

    # =====================================
    # BOSS MODE
    # =====================================
    if score > 0 and score % 30 == 0 and not boss_mode:

        boss_mode = True

        boss = pygame.Rect(
            WIDTH // 2 - 120,
            50,
            240,
            120
        )

    # =====================================
    # MOVE BULLETS
    # =====================================
    for bullet in bullets[:]:

        bullet.y -= 15

        if bullet.y < 0:
            bullets.remove(bullet)

    # =====================================
    # PLAYER RECT
    # =====================================
    player_rect = pygame.Rect(player_x, player_y, 70, 70)

    # =====================================
    # MOVE ENEMIES
    # =====================================
    for enemy in enemies[:]:

        enemy.y += enemy_speed

        # Enemy AI movement
        enemy.x += random.randint(-2, 2)

        if enemy.y > HEIGHT:

            enemies.remove(enemy)

            if player_shield > 0:
                player_shield -= 10
            else:
                player_health -= 10

        # Enemy shooting
        if random.randint(1, 100) == 1:

            enemy_bullets.append(
                pygame.Rect(enemy.x + 30, enemy.y + 60, 6, 20)
            )

        # Bullet collision
        for bullet in bullets[:]:

            if enemy.colliderect(bullet):

                create_explosion(enemy.x, enemy.y)

                if enemy in enemies:
                    enemies.remove(enemy)

                if bullet in bullets:
                    bullets.remove(bullet)

                score += 1
                coins += 5

                # Level system
                if score % 10 == 0:
                    level += 1
                    enemy_speed += 0.5

                break

        # Collision with player
        if enemy.colliderect(player_rect):

            create_explosion(player_x, player_y, 50)

            if player_shield > 0:
                player_shield -= 20
            else:
                player_health -= 20

            enemies.remove(enemy)

    # =====================================
    # ENEMY BULLETS
    # =====================================
    for ebullet in enemy_bullets[:]:

        ebullet.y += 10

        pygame.draw.rect(screen, RED, ebullet)

        if ebullet.y > HEIGHT:
            enemy_bullets.remove(ebullet)

        if ebullet.colliderect(player_rect):

            create_explosion(player_x, player_y, 20)

            if player_shield > 0:
                player_shield -= 10
            else:
                player_health -= 10

            enemy_bullets.remove(ebullet)

    # =====================================
    # BOSS LOGIC
    # =====================================
    if boss_mode:

        pygame.draw.rect(
            screen,
            PURPLE,
            boss,
            border_radius=20
        )

        glow_text(
            "BOSS",
            small_font,
            WHITE,
            boss.x + 80,
            boss.y + 40
        )

        # Boss shooting
        if random.randint(1, 20) == 1:

            enemy_bullets.append(
                pygame.Rect(boss.x + 120, boss.y + 100, 10, 30)
            )

        # Boss collision
        for bullet in bullets[:]:

            if boss.colliderect(bullet):

                boss_health -= 5

                create_explosion(bullet.x, bullet.y, 10)

                bullets.remove(bullet)

        # Boss health bar
        pygame.draw.rect(screen, RED, (350, 20, 500, 25))

        pygame.draw.rect(
            screen,
            GREEN,
            (350, 20, boss_health * 1.6, 25)
        )

        # Boss defeated
        if boss_health <= 0:

            create_explosion(boss.x + 100, boss.y + 50, 100)

            boss_mode = False
            boss_health = 300
            score += 20

    # =====================================
    # ENERGY BOOSTERS
    # =====================================
    for booster in energy_boosters[:]:

        booster.y += 4

        # Outer glow
        pygame.draw.circle(
            screen,
            CYAN,
            (booster.x + 20, booster.y + 20),
            22
        )

        # Inner glow
        pygame.draw.circle(
            screen,
            WHITE,
            (booster.x + 20, booster.y + 20),
            10
        )

        # Plus symbol
        pygame.draw.line(
            screen,
            BLUE,
            (booster.x + 20, booster.y + 6),
            (booster.x + 20, booster.y + 34),
            4
        )

        pygame.draw.line(
            screen,
            BLUE,
            (booster.x + 6, booster.y + 20),
            (booster.x + 34, booster.y + 20),
            4
        )

        if booster.y > HEIGHT:
            energy_boosters.remove(booster)

        # Collision with player
        if booster.colliderect(player_rect):

            player_health = min(100, player_health + 25)
            player_shield = min(50, player_shield + 15)

            create_explosion(
                booster.x,
                booster.y,
                25
            )

            energy_boosters.remove(booster)

    # =====================================
    # DRAW PLAYER SHIP
    # =====================================
    pygame.draw.polygon(
        screen,
        BLUE,
        [
            (player_x + 35, player_y),
            (player_x, player_y + 70),
            (player_x + 70, player_y + 70)
        ]
    )

    # Ship glow
    pygame.draw.circle(
        screen,
        CYAN,
        (player_x + 35, player_y + 45),
        8
    )

    # Engine flames
    flame = random.randint(10, 18)

    pygame.draw.circle(
        screen,
        ORANGE,
        (player_x + 35, player_y + 78),
        flame
    )

    # =====================================
    # DRAW BULLETS
    # =====================================
    for bullet in bullets:

        pygame.draw.rect(
            screen,
            GREEN,
            bullet,
            border_radius=10
        )

    # =====================================
    # DRAW ENEMIES
    # =====================================
    for enemy in enemies:

        pygame.draw.rect(
            screen,
            RED,
            enemy,
            border_radius=15
        )

        pygame.draw.circle(
            screen,
            YELLOW,
            (enemy.x + 20, enemy.y + 20),
            6
        )

        pygame.draw.circle(
            screen,
            YELLOW,
            (enemy.x + 50, enemy.y + 20),
            6
        )

    # =====================================
    # PARTICLE EFFECTS
    # =====================================
    for particle in particles[:]:

        particle[0] += particle[2]
        particle[1] += particle[3]
        particle[4] -= 0.15

        pygame.draw.circle(
            screen,
            random.choice([RED, YELLOW, WHITE, ORANGE]),
            (int(particle[0]), int(particle[1])),
            max(1, int(particle[4]))
        )

        if particle[4] <= 0:
            particles.remove(particle)

    # =====================================
    # UI PANEL
    # =====================================
    pygame.draw.rect(
        screen,
        (15, 15, 30),
        (0, 0, WIDTH, 85)
    )

    glow_text(
        f"Score : {score}",
        small_font,
        GREEN,
        20,
        20
    )

    glow_text(
        f"Coins : {coins}",
        small_font,
        YELLOW,
        200,
        20
    )

    glow_text(
        f"Level : {level}",
        small_font,
        BLUE,
        380,
        20
    )

    glow_text(
        f"Enemies : {len(enemies)}",
        small_font,
        RED,
        560,
        20
    )

    glow_text(
        "Energy Boosters Active",
        small_font,
        CYAN,
        20,
        55
    )

    # HEALTH BAR
    pygame.draw.rect(screen, RED, (850, 15, 250, 20))

    pygame.draw.rect(
        screen,
        GREEN,
        (850, 15, player_health * 2.5, 20)
    )

    glow_text(
        "HEALTH",
        small_font,
        WHITE,
        920,
        40
    )

    # SHIELD BAR
    pygame.draw.rect(screen, WHITE, (850, 65, 250, 15))

    pygame.draw.rect(
        screen,
        CYAN,
        (850, 65, player_shield * 5, 15)
    )

    # =====================================
    # GAME OVER
    # =====================================
    if player_health <= 0:
        game_over = True

    if game_over:

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)

        screen.blit(overlay, (0, 0))

        glow_text(
            "MISSION FAILED",
            title_font,
            RED,
            320,
            220
        )

        glow_text(
            f"FINAL SCORE : {score}",
            font,
            WHITE,
            430,
            340
        )

        glow_text(
            f"TOTAL COINS : {coins}",
            font,
            YELLOW,
            430,
            390
        )

        glow_text(
            "PRESS R TO RESTART",
            font,
            GREEN,
            360,
            470
        )

        if keys[pygame.K_r]:

            bullets.clear()
            enemy_bullets.clear()
            enemies.clear()
            particles.clear()
            powerups.clear()
            energy_boosters.clear()

            score = 0
            coins = 0
            level = 1

            player_health = 100
            player_shield = 50

            enemy_speed = 4

            boss_mode = False
            boss_health = 300

            game_over = False

    # =====================================
    # UPDATE DISPLAY
    # =====================================
    pygame.display.update()

pygame.quit()