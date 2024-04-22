import random
import sys

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pygame
pygame.init()

from config import Game_Config,Vehicle_config,Weather_config

from progress.vehicle import Main_vehicle
from progress.weather import Main_Weather

###################################################

# Kích thước của sổ 
SCREEN = pygame.display.set_mode([Game_Config.WIDTH, Game_Config.HEIGHT])

# Tốc độ làm mới màn hình 
clock = pygame.time.Clock()

# Hình nền ban đầu 
BACKGROUND = pygame.transform.scale(pygame.image.load(Game_Config.BACK_GROUND),(Game_Config.WIDTH,Game_Config.HEIGHT))


# Điểm ban đầu
Point = 0 

#Biến khác 

run_vehicle = 0
count_vehicle = 1
run_weather = 0
count_weather = 1
time = 0




###################### CHẠY GAME #############################

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()        
            
    # HIỂN THỊ HÌNH NỀN 
    SCREEN.blit(BACKGROUND,(0,0))

   

    # -------------------------------------- Phương tiện --------------------------------
    
    # THỜI GIAN XUẤT HIỆN THÊM 1 PHƯƠNG TIỆN     
    if count_vehicle < Vehicle_config.DELAY:
        time += 1
        if time==Vehicle_config.DELAY:           
            time=0
            count_vehicle += 1 

    
    # HÀM TẠO PHƯƠNG TIỆN 
    def create_vehicle(i,y1,y2):        

        # Thông tin phương tiện 
        Main_vehicle.LIST_VEHICLE[i][0] = random.choice(Main_vehicle.LIST_NAME_VEHICLE)

        # Tọa độ nhân vật xuất hiện
        Main_vehicle.LIST_VEHICLE[i][1] = random.choice([-100,Game_Config.WIDTH+100])
        Main_vehicle.LIST_VEHICLE[i][2] = random.randint(y1,y2)     

        # Hướng di chuyển 
        if Main_vehicle.LIST_VEHICLE[i][1] == -100:
            Main_vehicle.LIST_VEHICLE[i][3] = "Left"
        else:
            Main_vehicle.LIST_VEHICLE[i][3] = "Right"

        # Tốc độ di chuyển
        Main_vehicle.LIST_VEHICLE[i][4] = float(Main_vehicle.LIST_VEHICLE[i][0].split('.')[0].split('_')[1].replace('-', '.'))


    # TẠO PHƯƠNG TIỆN BAN ĐẦU     
    if run_vehicle < Vehicle_config.NUMBER:  
        create_vehicle(run_vehicle,Game_Config.HEIGHT-200,Game_Config.HEIGHT-100)     
        if run_vehicle == Vehicle_config.NUMBER - 1 :
            for i in range(Vehicle_config.NUMBER):
                for j in range(i + 1, Vehicle_config.NUMBER):
                   if  Main_vehicle.LIST_VEHICLE[i][2] > Main_vehicle.LIST_VEHICLE[j][2]:
                        tmp = Main_vehicle.LIST_VEHICLE[i][2]
                        Main_vehicle.LIST_VEHICLE[i][2] = Main_vehicle.LIST_VEHICLE[j][2]
                        Main_vehicle.LIST_VEHICLE[j][2] = tmp        
        run_vehicle += 1   


    # HIỂN THỊ VÀ DI CHUYỂN PHƯƠNG TIỆN
    if run_vehicle == Vehicle_config.NUMBER: 
        for i in range(count_vehicle):
            # Nếu phương tiện vẫn còn trong màn hình thì di chuyển:  
            if Main_vehicle.LIST_VEHICLE[i][1] <= Game_Config.WIDTH + 200 and Main_vehicle.LIST_VEHICLE[i][1] >= -200:           
              
                # Nếu phương tiện xuất hiện từ bên trái thì phương tiện di chuyển từ trái sang phải 
                if Main_vehicle.LIST_VEHICLE[i][3] == "Left":           
                    Main_vehicle.LIST_VEHICLE[i][1] = Main_vehicle.LIST_VEHICLE[i][1] +  Main_vehicle.LIST_VEHICLE[i][4]     
                    SCREEN.blit(pygame.transform.scale(pygame.image.load('pic/Vehicle_speed/'+Main_vehicle.LIST_VEHICLE[i][0]),(80,80)), ( Main_vehicle.LIST_VEHICLE[i][1], Main_vehicle.LIST_VEHICLE[i][2]))        

                # Nếu phương tiện xuất hiện từ bên phải thì phương tiện di chuyển từ phải sang trái 
                else:
                    Main_vehicle.LIST_VEHICLE[i][1] = Main_vehicle.LIST_VEHICLE[i][1] -  Main_vehicle.LIST_VEHICLE[i][4]
                    SCREEN.blit(pygame.transform.flip(pygame.transform.scale(pygame.image.load('pic/Vehicle_speed/'+Main_vehicle.LIST_VEHICLE[i][0]),(80,80)), True, False), ( Main_vehicle.LIST_VEHICLE[i][1], Main_vehicle.LIST_VEHICLE[i][2]))      


            # Nếu phương tiện không còn trong màn hình thì tạo thêm 1 phương tiện mới   
            else:
                if i == run_vehicle - 1:
                   create_vehicle(i,Main_vehicle.LIST_VEHICLE[i][2]-1,Game_Config.HEIGHT - 100)
                else:
                   create_vehicle(i,Main_vehicle.LIST_VEHICLE[i][2]-1,Main_vehicle.LIST_VEHICLE[i][2]+1) 



    # -------------------------------------- Thời tiết --------------------------------
    # HÀM TẠO THỜI TIẾT 
    def create_rain(i):
        # Loại thời tiết 
        Main_Weather.LIST_WEATHER[i][0] = random.choice(Main_Weather.LIST_NAME_WEATHER)
       
        # Tọa độ thời tiết xuất hiện 
        Main_Weather.LIST_WEATHER[i][1] = random.randint(100,Game_Config.WIDTH-100)
        Main_Weather.LIST_WEATHER[i][2] = 0


    # TẠO THỜI TIẾT BAN ĐẦU 
    if run_weather< Weather_config.NUMBER:
        create_rain(run_weather)
        run_weather += 1
    
    # HIỂN THỊ VÀ TẠO THỜI TIẾT 
    if run_weather == Weather_config.NUMBER:
        for i in range(count_weather):
            if Main_Weather.LIST_WEATHER[i][2] <= Game_Config.HEIGHT+100:             
                Main_Weather.LIST_WEATHER[i][2] += Weather_config.SPEED
                SCREEN.blit(pygame.transform.scale(pygame.image.load('pic/Weather/'+Main_Weather.LIST_WEATHER[i][0]),(40,40)), ( Main_Weather.LIST_WEATHER[i][1], Main_Weather.LIST_WEATHER[i][2]))


            else:
                # Trừ 1 điểm nếu người chơi đánh mất thời tiết cộng điểm và ngược lại 
                if Main_Weather.LIST_WEATHER[i][0].split('.')[0].split('_')[1] == "+Point":
                    Point -= 1
                else:
                    Point += 1

                create_rain(i)
            
            if count_weather < Weather_config.NUMBER and Main_Weather.LIST_WEATHER[i][2] >= Game_Config.HEIGHT/2 and i == count_weather - 1:
                count_weather += 1
    
    



    # -------------------------------------- Chuột người chơi --------------------------------
    # BIỂU TƯỢNG CHUỘT
    cursor_image = pygame.transform.scale(pygame.image.load("./pic/Umbrella/umbrella_1.png"),(70,70))
    cursor_in = cursor_image.get_rect()

    # TỌA ĐỘ CHUỘT 
    mouse_x, mouse_y = pygame.mouse.get_pos()


    # CẬP NHẬT VỊ TRÍ CHUỘT 
    cursor_in.center = (mouse_x, mouse_y)

    
    # HIỂN THỊ CHUỘT NGƯỜI CHƠI 
    SCREEN.blit(cursor_image, cursor_in)
        




    # -------------------------------------- Thời tiết và chuột người chơi --------------------------------
    for i in range(count_weather):
        # NẾU CON CHUỘT NGƯỜI CHƠI DI CHUỘT VÀO THỜI TIẾT THÌ
        if Main_Weather.LIST_WEATHER[i][1] - 80 < mouse_x < Main_Weather.LIST_WEATHER[i][1] + 80 and  Main_Weather.LIST_WEATHER[i][2] - 80 < mouse_y < Main_Weather.LIST_WEATHER[i][2] + 80:
            
            # Nếu người chơi di chuột vào thời tiết trừ điểm thì bị trừ 1 điểm 
            if Main_Weather.LIST_WEATHER[i][0].split('.')[0].split('_')[1] == "-Point":
                Point -= 1
            
            # Nếu người chơi di chuột vào thời tiết cộng điểm thì được cộng 1 điểm 
            else:
                Point += 1

            # Tạo 1 thời tiết để bù vào 
            create_rain(i)


    # -------------------------------------- Thời tiết và phương tiện --------------------------------
    for i in range(count_weather):
        for j in range (count_vehicle):
            if Main_vehicle.LIST_VEHICLE[j][1] - 50 < Main_Weather.LIST_WEATHER[i][1] < Main_vehicle.LIST_VEHICLE[j][1] + 50 and Main_vehicle.LIST_VEHICLE[j][2] - 50 < Main_Weather.LIST_WEATHER[i][2] < Main_vehicle.LIST_VEHICLE[j][2] + 50:
                
                # Nếu người chơi để thời tiết cộng điểm rơi mất và trúng vào phương tiện thì trừ 1 điểm
                if Main_Weather.LIST_WEATHER[i][0].split('.')[0].split('_')[1] == "+Point":
                    Point -= 1
                
                # Nếu người chơi để thời tiết trừ điểm rơi mất và trúng vào phương tiện thì cộng 1 điểm
                else:
                    Point += 1

                # Tạo 1 thời tiết để bù vào 
                create_rain(i)



    # -------------------------------------- Điểm số  --------------------------------
    font = pygame.font.Font(None, 36)
    text = font.render(f"Diem: {Point}", True, (0, 0, 0))
    SCREEN.blit(text, (100,100))








            
    # LÀM MỚI MÀN HÌNH        
    pygame.display.flip()
    clock.tick(Game_Config.FPS)




            


        
      







    







