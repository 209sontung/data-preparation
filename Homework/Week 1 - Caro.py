import numpy as np
import pygame, sys

pygame.init()

CARO_ROWS = 15
CARO_COLS = 15

font = pygame.font.Font('freesansbold.ttf', 20)
font12 = pygame.font.Font('freesansbold.ttf', 12)

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('CARO CHESS')
screen.fill((255,255,255))

caro = np.zeros((CARO_ROWS,CARO_COLS))

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_lines():
    i = 1
    while i <= 14:
        pygame.draw.line(screen, (124, 130, 125), (0, 53.3 * i), (800, 53.3 * i), 2)
        pygame.draw.line(screen, (124, 130, 125), (53.3 * i, 0), (53.3 * i, 800), 2)
        i += 1

def draw_player():
    for row in range(CARO_ROWS):
        for col in range(CARO_COLS):
            if caro[row][col] == 1:
                pygame.draw.line(screen, (207, 62, 62), (col * 53.3 + 10, row * 53.3 + 53.3 - 10), (col * 53.3 + 53.3 - 10, row * 53.3 + 10), 6)
                pygame.draw.line(screen, (207, 62, 62), (col * 53.3 + 10, row * 53.3 + 10), (col * 53.3 + 53.3 - 10, row * 53.3 + 53.3 - 10), 6)
            elif caro[row][col] == 2:
                pygame.draw.circle(screen, (68, 201, 91), (int(col * 53.3 + 26.5),int(row * 53.3 + 26.5)), 20, 5)

def mark_square(row, col, player):
    caro[row][col] = player

def is_available(row, col):
    return caro[row][col] == 0

def check_win(player, mi, mj):
    if check_win_vertical(player, mi, mj) or check_win_horizontal(player, mi, mj) or check_win_diogonal_1(player, mi, mj) or check_win_diogonal_2(player, mi, mj):
        return True
    else:
        return False

def check_win_vertical(player, mi, mj):
    i = mi - 1
    j = mj
    count = 0
    while i >= 0:
        if caro[i][j] == player:
            count += 1
        else:
            break
        i -= 1
    i = mi + 1
    j = mj
    while i < 15:
        if caro[i][j] == player:
            count += 1
        else:
            break
        i += 1
    if count >= 4:
        return True
    return False

def check_win_horizontal(player, mi, mj):
    i = mi
    j = mj - 1
    count = 0
    while j >= 0:
        if caro[i][j] == player:
            count += 1
        else:
            break
        j -= 1
    i = mi
    j = mj + 1
    while j < 15:
        if caro[i][j] == player:
            count += 1
        else:
            break
        j += 1
    if count >= 4:
        return True
    return False

def check_win_diogonal_1(player, mi, mj):
    i = mi - 1
    j = mj - 1
    count = 0
    while (i >= 0 and j >= 0):
        if caro[i][j] == player:
            count += 1
        else:
            break
        i -= 1
        j -= 1
    i = mi + 1
    j = mj + 1
    while (i < 15 and j < 15):
        if caro[i][j] == player:
            count += 1
        else:
            break
        i += 1
        j += 1
    if count >= 4:
        return True
    return False

def check_win_diogonal_2(player, mi, mj):
    i = mi - 1
    j = mj + 1
    count = 0
    while (i >= 0 and j < 15):
        if caro[i][j] == player:
            count += 1
        else:
            break
        i -= 1
        j += 1
    i = mi + 1
    j = mj - 1
    while (i < 15 and j >= 0):
        if caro[i][j] == player:
            count += 1
        else:
            break
        i += 1
        j -= 1
    if count >= 4:
        return True
    return False

def restart_game():
    screen.fill((255, 255, 255))
    draw_lines()
    for row in range(CARO_ROWS):
        for col in range(CARO_COLS):
            caro[row][col] = 0

draw_lines()

player = 1
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            clicked_row = int(mouseY // 53.3)
            clicked_col = int(mouseX // 53.3)

            if is_available(clicked_row, clicked_col):
                if player == 1:
                    mark_square(clicked_row, clicked_col, 1)
                    draw_player()
                    if check_win(player, clicked_row, clicked_col):
                        pygame.draw.rect(screen, (138, 133, 118), (300,0,200,80))
                        draw_text('X WIN!', font, (0, 0, 0), 365, 20)
                        draw_text('[PRESS R TO RESTART]!', font12, (0, 0, 0), 327, 50)
                        game_over = True
                    player = 2
                elif player == 2:
                    mark_square(clicked_row, clicked_col, 2)
                    draw_player()
                    if check_win(player, clicked_row, clicked_col):
                        pygame.draw.rect(screen, (138, 133, 118), (300, 0, 200, 80))
                        draw_text('O WIN!', font, (0, 0, 0), 365, 20)
                        draw_text('[PRESS R TO RESTART]!', font12, (0, 0, 0), 327, 50)
                        game_over = True
                    player = 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                player = 1
                game_over = False
    pygame.display.update()
