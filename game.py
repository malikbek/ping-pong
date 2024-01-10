import pygame
import sys

#звук в игре
pygame.mixer.init()
pygame.mixer.music.load("soundu.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play()


# Инициализация Pygame
pygame.init()

# Размеры экрана
screen_width = 600
screen_height = 400

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)

# Инициализация экрана
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Пинг-Понг")

# Инициализация ракеток и мяча
player1 = pygame.Rect(50, screen_height // 2 - 30, 10, 60)
player2 = pygame.Rect(screen_width - 60, screen_height // 2 - 30, 10, 60)
ball = pygame.Rect(screen_width // 2 - 10, screen_height // 2 - 10, 20, 20)

# Скорость мяча
ball_speed_x = 5
ball_speed_y = 5

# Скорость ракеток
player_speed = 10

# Инициализация бота
bot_speed = 6

# Счетчик очков
score_player1 = 0
score_player2 = 0

# Максимальное количество очков для завершения игры
max_score = 10

# Состояние игры
game_active = False
game_mode = None  # 0 - Играть, 1 - Игра на двоих, 2 - Игра с ботом

font = pygame.font.Font(None, 36)

def draw_menu():
    menu_text = ["1. Играть", "2. Игра на двоих", "3. Игра с ботом", "4. Выйти"]
    y = screen_height // 2 - len(menu_text) * 20
    for text in menu_text:
        text_surface = font.render(text, True, white)
        text_rect = text_surface.get_rect(center=(screen_width // 2, y))
        screen.blit(text_surface, text_rect)
        y += 40

def start_game(selected_mode):
    global game_active, game_mode, ball_speed_x, ball_speed_y, score_player1, score_player2
    game_active = True
    game_mode = selected_mode
    ball_speed_x = 5
    ball_speed_y = 5
    score_player1 = 0
    score_player2 = 0

def main_menu():
    while not game_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    start_game(0)
                elif event.key == pygame.K_2:
                    start_game(1)
                elif event.key == pygame.K_3:
                    start_game(2)
                elif event.key == pygame.K_4:
                    pygame.quit()
                    sys.exit()

        screen.fill(black)
        draw_menu()
        pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Управление первой ракеткой
    if game_mode == 0 or game_mode == 1:
        if keys[pygame.K_w] and player1.top > 0:
            player1.y -= player_speed
        if keys[pygame.K_s] and player1.bottom < screen_height:
            player1.y += player_speed

    # Управление второй ракеткой
    if game_mode == 0 or game_mode == 1:
        if keys[pygame.K_UP] and player2.top > 0:
            player2.y -= player_speed
        if keys[pygame.K_DOWN] and player2.bottom < screen_height:
            player2.y += player_speed
    elif game_mode == 2:  # Игра с ботом
        if ball.centery < player2.centery and player2.top > 0:
            player2.y -= bot_speed
        elif ball.centery > player2.centery and player2.bottom < screen_height:
            player2.y += bot_speed

    # Движение мяча
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Обработка столкновений с верхней и нижней стенками
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y = -ball_speed_y

    # Обработка столкновений с ракетками
    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_speed_x = -ball_speed_x

    # Проверка завершения игры
    if ball.left <= 0:
        score_player2 += 1
        ball.x = screen_width // 2 - 10
        ball.y = screen_height // 2 - 10
        if score_player2 == max_score:
            print("Игрок 2 выиграл!")
            pygame.mixer.music.load("lose.mp3")
            pygame.mixer.music.play()
            game_active = False
    elif ball.right >= screen_width:
        score_player1 += 1
        ball.x = screen_width // 2 - 10
        ball.y = screen_height // 2 - 10
        if score_player1 == max_score:
            print("Игрок 1 выиграл!")
            pygame.mixer.music.load("lose.mp3")
            pygame.mixer.music.play()
            game_active = False

    # Очистка экрана
    screen.fill(black)

    # Отрисовка ракеток и мяча
    pygame.draw.rect(screen, white, player1)
    pygame.draw.rect(screen, white, player2)
    pygame.draw.ellipse(screen, white, ball)

    # Отрисовка счета
    score_text = font.render(f"{score_player1} - {score_player2}", True, white)
    score_rect = score_text.get_rect(center=(screen_width // 2, 20))
    screen.blit(score_text, score_rect)

    # Отрисовка меню при неактивной игре
    if not game_active:
        main_menu()

    # Обновление экрана
    pygame.display.flip()

    # Задержка для контроля скорости обновления
    pygame.time.Clock().tick(60)