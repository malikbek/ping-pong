import pygame
import sys

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Инициализация окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-Понг")

# Инициализация мяча
ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
ball_speed = [5, 5]

# Инициализация ракеток
player = pygame.Rect(WIDTH - 20, HEIGHT // 2 - 50, 10, 100)
opponent = pygame.Rect(10, HEIGHT // 2 - 50, 10, 100)

# Основной цикл игры
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Управление ракеткой игрока
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
        player.y += 5
    if keys[pygame.K_UP] and player.top > 0:
        player.y -= 5

    # Движение мяча
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Отскок мяча от стен
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed[1] = -ball_speed[1]

    # Отскок мяча от ракеток
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed[0] = -ball_speed[0]

    # Движение ракетки оппонента
    if opponent.centery < ball.centery:
        opponent.y += 3
    elif opponent.centery > ball.centery:
        opponent.y -= 3

    # Отрисовка элементов
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, WHITE, opponent)
    pygame.draw.ellipse(screen, WHITE, ball)

    # Обновление экрана
    pygame.display.flip()

    # Задержка для контроля скорости
    pygame.time.Clock().tick(60)