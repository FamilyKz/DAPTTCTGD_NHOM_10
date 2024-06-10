import random
import sys
import os
import pygame
os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.init()

# Chèn các file python 
from config import Game_Config
from progress.vehicle import Main_vehicle, Vehicle_config 
from progress.level import select_level, generate_math_problem

# Thiết lập thông số game 
SCREEN = pygame.display.set_mode([Game_Config.WIDTH, Game_Config.HEIGHT])
clock = pygame.time.Clock()
BACKGROUND = pygame.transform.scale(pygame.image.load(Game_Config.BACK_GROUND), (Game_Config.WIDTH, Game_Config.HEIGHT))
LEVEL_BACKGROUND = pygame.transform.scale(pygame.image.load('pic/level.jpg'), (Game_Config.WIDTH, Game_Config.HEIGHT))

# Font chữ Tiếng Việt 
font = pygame.font.Font("./font/SVN-Times New Roman Bold.ttf", 30)

# Lấy cấp độ game 
selected_level = select_level(SCREEN, font, LEVEL_BACKGROUND)
a, b, operator, kq_ab = generate_math_problem(selected_level)

# Các biến khác 
Point = 0
HEAL = 3
run_vehicle = 0
count_vehicle = 0
time = 0
select_kq = " "
show_check_kq = False
game_over = False

# Hàm tạo màu nền cho chữ 
def draw_text_with_background(surface, text, font, color, background_color, pos):
    text_surface = font.render(text, True, color)
    background_rect = text_surface.get_rect(topleft=pos)
    pygame.draw.rect(surface, background_color, background_rect)
    surface.blit(text_surface, pos)

# Hàm tạo phương tiện 
def create_vehicle(i, y1, y2):
    global run_vehicle, count_vehicle, time
    Main_vehicle.LIST_VEHICLE[i][0] = random.choice(Main_vehicle.LIST_NAME_VEHICLE)
    Main_vehicle.LIST_VEHICLE[i][1] = random.choice([-100, Game_Config.WIDTH + 100])
    Main_vehicle.LIST_VEHICLE[i][2] = random.randint(y1, y2)
    
    if Main_vehicle.LIST_VEHICLE[i][1] == -100:
        Main_vehicle.LIST_VEHICLE[i][3] = "Left"
    else:
        Main_vehicle.LIST_VEHICLE[i][3] = "Right"

    Main_vehicle.LIST_VEHICLE[i][4] = float(Main_vehicle.LIST_VEHICLE[i][0].split('.')[0].split('_')[1].replace('-', '.'))
    
    if run_vehicle == 0:
        Main_vehicle.LIST_VEHICLE[i][5] = kq_ab
    else:
        count_kq = 0
        if not show_check_kq and run_vehicle == Vehicle_config.NUMBER:
            for x in range(count_vehicle):
                if Main_vehicle.LIST_VEHICLE[x][5] == kq_ab:
                    count_kq += 1
            if count_kq <= 1:
                Main_vehicle.LIST_VEHICLE[i][5] = kq_ab
                count_kq = 0
        else:
            Main_vehicle.LIST_VEHICLE[i][5] = random.randint(1, 100)

# Hàm chơi lại game 
def reset_game():
    global Point, HEAL, run_vehicle, count_vehicle, time, select_kq, show_check_kq, game_over, selected_level, a, b, operator, kq_ab
    Point = 0
    HEAL = 3
    run_vehicle = 0
    count_vehicle = 0
    time = 0
    select_kq = " "
    show_check_kq = False
    game_over = False
    selected_level = select_level(SCREEN, font, LEVEL_BACKGROUND)
    a, b, operator, kq_ab = generate_math_problem(selected_level)

# Chạy game 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                reset_game()

    # Game logic
    if not game_over:
        if HEAL <= 0:
            game_over = True
        
        # Hiển thị hình nền và chữ ban đầu 
        SCREEN.blit(BACKGROUND, (0, 0))
        draw_text_with_background(SCREEN, "Phép toán", font, (0, 0, 0), (255, 255, 255), (Game_Config.WIDTH // 2, 50))
        draw_text_with_background(SCREEN, f"{a} {operator} {b} = {select_kq}", font, (0, 0, 0), (255, 255, 255), (Game_Config.WIDTH // 2, 100))
        
        if show_check_kq:
            draw_text_with_background(SCREEN, "Sai", font, (255, 0, 0), (255, 255, 255), (Game_Config.WIDTH // 2 + 30, 150))

        # Hàm di chuyển phương tiện 
        if count_vehicle < Vehicle_config.DELAY:
            time += 1
            if time == Vehicle_config.DELAY:
                time = 0
                if count_vehicle < Vehicle_config.NUMBER:
                    count_vehicle += 1

        if run_vehicle < Vehicle_config.NUMBER:
            create_vehicle(run_vehicle, Game_Config.HEIGHT - 200, Game_Config.HEIGHT - 100)
            if run_vehicle == Vehicle_config.NUMBER - 1:
                for i in range(Vehicle_config.NUMBER):
                    for j in range(i + 1, Vehicle_config.NUMBER):
                        if Main_vehicle.LIST_VEHICLE[i][2] > Main_vehicle.LIST_VEHICLE[j][2]:
                            tmp = Main_vehicle.LIST_VEHICLE[i][2]
                            Main_vehicle.LIST_VEHICLE[i][2] = Main_vehicle.LIST_VEHICLE[j][2]
                            Main_vehicle.LIST_VEHICLE[j][2] = tmp
            run_vehicle += 1

        if run_vehicle == Vehicle_config.NUMBER:
            for i in range(count_vehicle):
                if -200 <= Main_vehicle.LIST_VEHICLE[i][1] <= Game_Config.WIDTH + 200:
                    if Main_vehicle.LIST_VEHICLE[i][3] == "Left":
                        Main_vehicle.LIST_VEHICLE[i][1] += Main_vehicle.LIST_VEHICLE[i][4]
                        SCREEN.blit(pygame.transform.scale(pygame.image.load('pic/Vehicle_speed/' + Main_vehicle.LIST_VEHICLE[i][0]), (80, 80)), (Main_vehicle.LIST_VEHICLE[i][1], Main_vehicle.LIST_VEHICLE[i][2]))
                        draw_text_with_background(SCREEN, f"{Main_vehicle.LIST_VEHICLE[i][5]}", font, (0, 0, 0), (255, 255, 255), (Main_vehicle.LIST_VEHICLE[i][1] + 30, Main_vehicle.LIST_VEHICLE[i][2] - 30))
                    else:
                        Main_vehicle.LIST_VEHICLE[i][1] -= Main_vehicle.LIST_VEHICLE[i][4]
                        SCREEN.blit(pygame.transform.flip(pygame.transform.scale(pygame.image.load('pic/Vehicle_speed/' + Main_vehicle.LIST_VEHICLE[i][0]), (80, 80)), True, False), (Main_vehicle.LIST_VEHICLE[i][1], Main_vehicle.LIST_VEHICLE[i][2]))
                        draw_text_with_background(SCREEN, f"{Main_vehicle.LIST_VEHICLE[i][5]}", font, (0, 0, 0), (255, 255, 255), (Main_vehicle.LIST_VEHICLE[i][1] + 30, Main_vehicle.LIST_VEHICLE[i][2] - 30))
                    

                    # Sự kiện click chuột vào phương tiện -> Check đáp án 
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if Main_vehicle.LIST_VEHICLE[i][1] - 80 < mouse_x < Main_vehicle.LIST_VEHICLE[i][1] + 80 and Main_vehicle.LIST_VEHICLE[i][2] - 80 < mouse_y < Main_vehicle.LIST_VEHICLE[i][2] + 80:
                            select_kq = Main_vehicle.LIST_VEHICLE[i][5]

                            if select_kq == kq_ab:
                                show_check_kq = False
                                Point += 1
                                a, b, operator, kq_ab = generate_math_problem(selected_level)
                                select_kq = " "
                            else:
                                show_check_kq = True
                                HEAL -= 1

                            if i == run_vehicle - 1:
                                create_vehicle(i, Main_vehicle.LIST_VEHICLE[i][2] - 1, Game_Config.HEIGHT - 100)
                            else:
                                create_vehicle(i, Main_vehicle.LIST_VEHICLE[i][2] - 1, Main_vehicle.LIST_VEHICLE[i][2] + 1)
                else:
                    if i == run_vehicle - 1:
                        create_vehicle(i, Main_vehicle.LIST_VEHICLE[i][2] - 1, Game_Config.HEIGHT - 100)
                    else:
                        create_vehicle(i, Main_vehicle.LIST_VEHICLE[i][2] - 1, Main_vehicle.LIST_VEHICLE[i][2] + 1)

        draw_text_with_background(SCREEN, f"Mạng: {HEAL}", font, (0, 0, 0), (255, 255, 255), (100, 50))
        draw_text_with_background(SCREEN, f"Điểm: {Point}", font, (0, 0, 0), (255, 255, 255), (100, 100))

    else:
        SCREEN.blit(BACKGROUND, (0, 0))
        draw_text_with_background(SCREEN, "Game Over", font, (255, 0, 0), (255, 255, 255), (Game_Config.WIDTH // 2 - 50, Game_Config.HEIGHT // 2 - 50))
        draw_text_with_background(SCREEN, "Press 'R' to Restart", font, (0, 0, 0), (255, 255, 255), (Game_Config.WIDTH // 2 - 100, Game_Config.HEIGHT // 2))

    pygame.display.flip()
    clock.tick(Game_Config.FPS)
