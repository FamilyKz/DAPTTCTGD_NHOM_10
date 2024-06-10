import pygame
import sys
import random
from config import Game_Config

# Các cấp độ của trò chơi
LEVELS = {
    1: (2, 10),
    2: (10, 50),
    3: (50, 100)
}

# Hàm tạo màn hình chọn cấp độ
def select_level(screen, font, background_image):
    # Vị trí các nút
    button_positions = [
        (Game_Config.WIDTH // 2, Game_Config.HEIGHT // 2 - 220),
        (Game_Config.WIDTH // 2, Game_Config.HEIGHT // 2 - 160),
        (Game_Config.WIDTH // 2, Game_Config.HEIGHT // 2 - 100)
    ]
    button_texts = ["1. Dễ", "2. Trung bình", "3. Khó"]
    button_rects = []

    while True:
        screen.blit(background_image, (0, 0))
        draw_text(screen, "Chọn cấp độ", font, (0, 0, 0), (Game_Config.WIDTH // 2, Game_Config.HEIGHT // 2 - 300))

        mouse_pos = pygame.mouse.get_pos()

        for i, pos in enumerate(button_positions):
            if pygame.Rect(pos[0] - 50, pos[1] - 20, 100, 40).collidepoint(mouse_pos):
                color = (200, 200, 200)  # Màu sáng khi di chuột vào
            else:
                color = (255, 255, 255)  # Màu nền bình thường

            button_rect = draw_text(screen, button_texts[i], font, (0, 0, 0), pos, background_color=color)
            button_rects.append(button_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                elif event.key == pygame.K_2:
                    return 2
                elif event.key == pygame.K_3:
                    return 3
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, button_rect in enumerate(button_rects):
                    if button_rect.collidepoint(mouse_pos):
                        return i + 1

# Hàm vẽ văn bản và trả về hình chữ nhật chứa văn bản
def draw_text(screen, text, font, color, pos, background_color=None):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=pos)
    if background_color:
        pygame.draw.rect(screen, background_color, text_rect.inflate(20, 10))
    screen.blit(text_surface, text_rect)
    return text_rect


# Hàm tạo bài toán dựa trên cấp độ

def generate_math_problem(level):
    min_val, max_val = LEVELS[level]
    a = random.randint(min_val, max_val)
    b = random.randint(min_val, max_val)
    a_b = random.choice(['+', '-', 'x', '%'])

    kq_ab = 0
    
    if a_b == "+":
        kq_ab = a + b
    elif a_b == "x":
        kq_ab = a * b


    elif a_b == "-":
        if a >= b:
            kq_ab = a - b
        else:
            a, b = b, a
            kq_ab = a - b

    elif a_b == "%":
        if a % b != 0:
            a = a * b 
            b = a / b           
            kq_ab = a / b   
    a = int(a)
    b = int(b)
    kq_ab = int(kq_ab)
    
    return a, b, a_b, kq_ab
