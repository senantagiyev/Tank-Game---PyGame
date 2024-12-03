import pygame
import random
import sys

# Pygame'i başlat
pygame.init()

# Ekran boyutları
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tank Oyunu")

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# FPS Kontrolü
clock = pygame.time.Clock()

# Arka Plan
background = pygame.image.load('background.jpg')  # Arka plan resmi
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Patlama efekti
explosion_image = pygame.image.load('explosion.png')  # Patlama resmi
explosion_image = pygame.transform.scale(explosion_image, (100, 100))

# Tank (silah) ve düşman tankı görselleri
tank_image = pygame.image.load('tank.png')  # Oyuncunun tankı
tank_image = pygame.transform.scale(tank_image, (60, 60))

enemy_tank_image = pygame.image.load('enemy_tank.png')  # Düşman tankı
enemy_tank_image = pygame.transform.scale(enemy_tank_image, (60, 60))

# Silah
gun_width = 60
gun_height = 60
gun_x = SCREEN_WIDTH // 2 - gun_width // 2
gun_y = SCREEN_HEIGHT - gun_height - 10
gun_speed = 5

# Mermi
bullet_width = 10
bullet_height = 20
bullet_speed = 2  # Mermilerin hızını daha da yavaşlattık
bullets = []

# Hedefler
target_width = 60
target_height = 60
targets = []

# Hedef mermileri
target_bullets = []
target_bullet_speed = 3  # Hedef mermilerinin hızını yavaşlattık

# Can
lives = 3
font = pygame.font.SysFont('Arial', 30)

# Puan
score = 0

# Hedefleri yarat
def create_target():
    x = random.randint(0, SCREEN_WIDTH - target_width)
    y = random.randint(50, 150)
    return pygame.Rect(x, y, target_width, target_height)

# Hedef mermisi oluştur
def create_target_bullet(target_x, target_y):
    return pygame.Rect(target_x + target_width // 2 - bullet_width // 2, target_y + target_height, bullet_width, bullet_height)

# Silahı çiz
def draw_gun():
    screen.blit(tank_image, (gun_x, gun_y))

def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, RED, bullet)

def draw_targets():
    for target in targets:
        screen.blit(enemy_tank_image, (target.x, target.y))

def draw_target_bullets():
    for bullet in target_bullets:
        pygame.draw.rect(screen, BLUE, bullet)

def draw_explosion(x, y):
    screen.blit(explosion_image, (x - explosion_image.get_width() // 2, y - explosion_image.get_height() // 2))

def check_collisions():
    global lives, score
    for bullet in bullets[:]:
        for target in targets[:]:
            if bullet.colliderect(target):
                bullets.remove(bullet)
                targets.remove(target)
                targets.append(create_target())  
                score += 1  
                break

    for target_bullet in target_bullets[:]:
        if target_bullet.colliderect(pygame.Rect(gun_x, gun_y, gun_width, gun_height)):
            target_bullets.remove(target_bullet)
            lives -= 1  
            return True  
    return False

def game_loop():
    global gun_x, gun_y, bullets, targets, lives, score, target_bullets

    if not targets:
        targets.append(create_target())

    while True:
        screen.fill(WHITE)

        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                bullet = pygame.Rect(gun_x + gun_width // 2 - bullet_width // 2, gun_y, bullet_width, bullet_height)
                bullets.append(bullet)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and gun_x > 0:  
            gun_x -= gun_speed
        if keys[pygame.K_d] and gun_x < SCREEN_WIDTH - gun_width:  
            gun_x += gun_speed
        if keys[pygame.K_w] and gun_y > 0:  
            gun_y -= gun_speed
        if keys[pygame.K_s] and gun_y < SCREEN_HEIGHT - gun_height:  
            gun_y += gun_speed

        for target in targets:
            target.x += random.choice([-1, 1]) * random.randint(1, 3)
            target.y += random.choice([-1, 1]) * random.randint(1, 3)

        for target in targets:
            if random.random() < 0.02:  
                target_bullets.append(create_target_bullet(target.x, target.y))

        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.y < 0:
                bullets.remove(bullet)

        for target_bullet in target_bullets[:]:
            target_bullet.y += target_bullet_speed
            if target_bullet.y > SCREEN_HEIGHT:
                target_bullets.remove(target_bullet)

        if check_collisions():
            draw_explosion(gun_x + gun_width // 2, gun_y + gun_height // 2)

        if score % 5 == 0: 
            target_count = len(targets)
            if target_count == 1:
                targets.append(create_target()) 
            elif target_count == 2:
                targets.append(create_target()) 
            elif target_count == 4:
                targets.append(create_target())  

        draw_gun()
        draw_bullets()
        draw_targets()
        draw_target_bullets()

        score_text = font.render(f"Xal: {score}", True, BLACK)
        lives_text = font.render(f"Can: {lives}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))

        if lives <= 0:
            game_over_text = font.render("GAME OVER", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(2000)  
            pygame.quit()
            sys.exit()

        pygame.display.flip()

        clock.tick(60)

game_loop()
