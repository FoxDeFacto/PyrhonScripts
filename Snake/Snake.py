import pygame
import random
import sys

# Inicializace Pygame
pygame.init()
pygame.mixer.init()

# Barvy
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Nastavení okna
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Had")

# Nastavení hry
SNAKE_BLOCK = 20
SNAKE_SPEEDS = {"Lehká": 10, "Střední": 15, "Těžká": 20}

# Fonty
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Načtení nejlepšího skóre
try:
    with open("highscore.txt", "r") as f:
        high_score = int(f.read())
except FileNotFoundError:
    high_score = 0

def draw_snake(snake_block, snake_list):
    for i, x in enumerate(snake_list):
        color = (0, max(255 - i * 5, 50), 0)  # Gradient efekt
        pygame.draw.rect(window, color, [x[0], x[1], snake_block, snake_block])
        pygame.draw.rect(window, (0, min(255, 100 + i * 5), 0), [x[0], x[1], snake_block, snake_block], 1)

def draw_food(x, y):
    pygame.draw.circle(window, RED, (x + SNAKE_BLOCK // 2, y + SNAKE_BLOCK // 2), SNAKE_BLOCK // 2)

def message(msg, color, y_displace=0):
    mesg = font.render(msg, True, color)
    window.blit(mesg, [WIDTH // 2 - mesg.get_width() // 2, HEIGHT // 2 - mesg.get_height() // 2 + y_displace])

def score(score):
    value = font.render("Skóre: " + str(score), True, WHITE)
    window.blit(value, [10, 10])

def draw_menu():
    window.fill(BLACK)
    title = large_font.render("Had", True, GREEN)
    window.blit(title, [WIDTH // 2 - title.get_width() // 2, 100])
    
    buttons = [("Hrát", 250), ("Obtížnost", 320), ("Konec", 390)]
    for text, y in buttons:
        button = font.render(text, True, WHITE)
        button_rect = button.get_rect(center=(WIDTH // 2, y))
        window.blit(button, button_rect)
        
    pygame.display.update()

def difficulty_menu():
    difficulty = "Medium"
    while True:
        window.fill(BLACK)
        title = large_font.render("Obtížnost", True, GREEN)
        window.blit(title, [WIDTH // 2 - title.get_width() // 2, 100])
        
        buttons = [("Lehká", 250), ("Střední", 320), ("Těžká", 390), ("Zpět", 460)]
        for text, y in buttons:
            color = GREEN if text == difficulty else WHITE
            button = font.render(text, True, color)
            button_rect = button.get_rect(center=(WIDTH // 2, y))
            window.blit(button, button_rect)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for text, y in buttons:
                    button_rect = pygame.Rect(0, 0, 200, 50)
                    button_rect.center = (WIDTH // 2, y)
                    if button_rect.collidepoint(mouse_pos):
                        if text == "Zpět":
                            return difficulty
                        else:
                            difficulty = text

def gameLoop(difficulty):
    global high_score
    game_over = False
    game_paused = False

    x1 = WIDTH / 2
    y1 = HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK
    foody = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK

    clock = pygame.time.Clock()
    score_value = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_p:
                    game_paused = not game_paused

        if game_paused:
            message("Hra pozastavena. Stiskněte P pro pokračování.", WHITE)
            pygame.display.update()
            continue

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_over = True

        x1 += x1_change
        y1 += y1_change

        window.fill(BLACK)
        draw_food(foodx, foody)
        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_over = True

        draw_snake(SNAKE_BLOCK, snake_list)
        score(score_value)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK
            foody = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK
            length_of_snake += 1
            score_value += 10

        clock.tick(SNAKE_SPEEDS[difficulty])

    if score_value > high_score:
        high_score = score_value
        with open("highscore.txt", "w") as f:
            f.write(str(high_score))

    window.fill(BLACK)
    message("Konec hry!", RED, -50)
    message(f"Skóre: {score_value}", WHITE, 0)
    message(f"Nejlepší skóre: {high_score}", WHITE, 50)
    message("Stiskněte Q pro ukončení nebo C pro novou hru", WHITE, 100)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                if event.key == pygame.K_c:
                    return True

def main():
    difficulty = "Medium"
    while True:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH // 2 - 50 <= mouse_pos[0] <= WIDTH // 2 + 50:
                    if 230 <= mouse_pos[1] <= 270:  # Hrát
                        if gameLoop(difficulty):
                            continue
                        else:
                            pygame.quit()
                            sys.exit()
                    elif 300 <= mouse_pos[1] <= 340:  # Obtížnost
                        difficulty = difficulty_menu()
                    elif 370 <= mouse_pos[1] <= 410:  # Konec
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    main()