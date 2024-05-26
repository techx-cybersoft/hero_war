import pygame
import sys
import random


pygame.init()
#Khởi tạo cửa sổ game và tên game
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jackie the superhuman")

#Tạo font chữ
f_game = pygame.font.Font('./fonts/font_game.otf', 32)

#Tạo surface đưa lên giao diện
score = 0
score_text = f_game.render(f"score {score}", True, "Red", "White")
score_x = SCREEN_WIDTH - score_text.get_width() - 100
score_y = 0 

#Surface ảnh
#Background
bg_game = pygame.image.load("./img/bg_game.jpg")
bg_game = pygame.transform.scale(bg_game, (SCREEN_WIDTH, SCREEN_HEIGHT))
#Hero
hero = pygame.image.load("./img/player.png")
hero = pygame.transform.scale(hero, (150, 71.67))
hero_rect = hero.get_rect()
#Bullet
bullet = pygame.image.load("./img/bullet.png")
bullet = pygame.transform.scale(bullet, (80, 51.87))
bullet_rect = bullet.get_rect()
bullet_rect.x = 200
bullet_rect.y = 0
#Gem
gem = pygame.image.load("./img/gem.png")
gem = pygame.transform.scale(gem, (80, 61.7))
gem_rect = gem.get_rect()
#Setup tọa độ gem (trong khung hình)
gem_rect.x = random.randint(gem.get_width(), SCREEN_WIDTH - gem.get_width())
gem_rect.y = random.randint(gem.get_height(), SCREEN_HEIGHT - gem.get_height())

#setup khung hình
clock = pygame.time.Clock()
#Danh sách các biến hằng số
speed_hero = 10
speed_bullet = 10

#Xử lý thời gian
time_start = 0
time_text = f_game.render(f"Time {time_start}", True, "Orange")
time_x = SCREEN_WIDTH // 2
time_y = 0 

#Xử lý âm thanh
nhac_nen = pygame.mixer.Sound('./sounds/typical-trap-loop-2b-130751.wav')
sound_dan_ban = pygame.mixer.Sound('./sounds/whoosh-cinematic-161021.wav')
va_cham = pygame.mixer.Sound('./sounds/vine-boom-162668.wav')
nhac_nen.play(-1)

time_start_bullet = 0

#Tạo surface text về mạng
live = 2
live_text = f_game.render(f"Live {live}", True, "Orange")
live_x = 0
live_y = 0

#Vòng lặp game
running = True

while running:
    
    """current_time = pygame.time.get_ticks() // 1000 
    if current_time % 10 == 0:
        gem_rect.x = random.randint(gem.get_width(), SCREEN_WIDTH - gem.get_width())
        gem_rect.y = random.randint(gem.get_height(), SCREEN_HEIGHT - gem.get_height())"""
    
    #Cài đặt game
    #events: hành động bấm từng phím hoặc click từng nháy
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Bắn đạn = phím space
                bullet_rect.x = hero_rect.x + hero.get_width()
                bullet_rect.y = hero_rect.y + hero.get_height() / 2
                #Phát nhạc bằng bắn đạn
                sound_dan_ban.play()
                
    bullet_rect.x += speed_bullet 
        
    # Cài đặt sự kiện đè phím cho nhân vật hero
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and hero_rect.y > 0: # Tất cả đều True thì mới làm
        hero_rect.y -= speed_hero
    elif keys[pygame.K_DOWN] and hero_rect.y <= SCREEN_HEIGHT - hero.get_height():
        hero_rect.y += speed_hero
    elif keys[pygame.K_LEFT] and hero_rect.x > 0:
        hero_rect.x -= speed_hero
    elif keys[pygame.K_RIGHT] and hero_rect.x <= SCREEN_WIDTH - hero.get_width():
        hero_rect.x += speed_hero
        
            
    #Blit bg
    WINDOW.blit(bg_game, (0,0))
    
    #Các phần kịch bản game
    WINDOW.blit(score_text, (score_x,score_y))
    #Hero
    WINDOW.blit(hero, (hero_rect.x, hero_rect.y))
    # pygame.draw.rect(WINDOW, "Pink", hero_rect, 2)
    #Bullet
    WINDOW.blit(bullet, (bullet_rect.x, bullet_rect.y))
    # pygame.draw.rect(WINDOW, "Orange", bullet_rect, 2)
    #Gem
    WINDOW.blit(gem, (gem_rect.x, gem_rect.y))
    # pygame.draw.rect(WINDOW, "Pink", gem_rect, 2)
    #Live 
    WINDOW.blit(live_text, (live_x, live_y))
    #Time
    #Tính toán thời gian
    current_time = pygame.time.get_ticks() // 1000 #1000 1001 ... n
    count_down = 10 - (current_time - time_start)
    if count_down <= 0:
        time_start = current_time
        #Cứ sau 10s đếm ngược thì trừ 1 mạng
        live -= 2
        live_text = f_game.render(f"Live {live}", True, "Orange")
            
    
    if live < 0:
        time_text = f_game.render("Game Over", True, "Red")
        WINDOW.blit(time_text, (time_x, time_y))
        pygame.display.flip()
        #Sau 3 giây thì ngừng game
        pygame.time.delay(3000)
        running = False
    
    time_text = f_game.render(f"Time {count_down}", True, "Orange")
    WINDOW.blit(time_text, (time_x, time_y))
    
    
    
    #Effect: Hiệu ứng
    time_current_bullet = pygame.time.get_ticks()
    time_bullet = time_current_bullet - time_start_bullet
    
    if time_bullet >= 100:
        if bullet_rect.colliderect(gem_rect): #Nếu hình chữ nhật đạn chạm hình chữ nhật viên ngọc
            #Tính và viết lại điểm
            score += 10
            score_text = f_game.render(f"score {score}", True, "Red", "White")
            #Xét lại vị trí của thiên thạch
            gem_rect.x = random.randint(gem.get_width(), SCREEN_WIDTH - gem.get_width())
            gem_rect.y = random.randint(gem.get_height(), SCREEN_HEIGHT - gem.get_height())
            #Xét lại tọa độ đạn
            bullet_rect.x = SCREEN_WIDTH + 100 
            #Lồng nhạc va chạm
            va_cham.play()
            #Xét lại thời gian
            time_start = current_time
        time_start_bullet = time_current_bullet
        
    #Cập nhật liên tục
    pygame.display.flip()
    clock.tick(60)
    
    
pygame.quit()
sys.exit()