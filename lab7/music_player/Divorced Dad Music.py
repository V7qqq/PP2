import pygame
import os
import sys

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 540, 830
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Divorced Dad Music")
BG_COLOR = (28, 27, 27)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (50, 50, 50)
BUTTON_HOVER = (80, 80, 80)
BUTTON_CLICK = (200, 200, 200)
BUTTON_DEFAULT = (180, 80, 80)

state = "animation"

avatar_path = os.path.join("фото", "ava3.png")
start_path = os.path.join("звуки", "start.mp3")
girlsound_path = os.path.join("звуки","girlsound.mp3")
girlsound = pygame.mixer.Sound(girlsound_path)
album_audio = os.path.join("музыка_фото", "аудио.jpg")
album_creed = os.path.join("музыка_фото", "крид.jpg")
album_mars = os.path.join("музыка_фото", "марс.jpg")
girl_images = [
    pygame.image.load(os.path.join("фото","девочка1.png")).convert_alpha(),
    pygame.image.load(os.path.join("фото","девочка2.png")).convert_alpha(),
]

girl_x = 100
girl_y = 10

girl_c = 0
girl = True
girl_timer = None

Vision = False
play_clicked = False
check = False
check_2 = False
play_icon = pygame.image.load(os.path.join("фото", "play.png")).convert_alpha()
pause_icon = pygame.image.load(os.path.join("фото", "pause.png")).convert_alpha()
play_icon = pygame.transform.scale(play_icon, (50, 50))
pause_icon = pygame.transform.scale(pause_icon, (50, 50))

avatar = pygame.image.load(avatar_path).convert_alpha()
start = pygame.mixer.Sound(start_path)
pygame.display.set_icon(avatar)

subscription_buttons = {
    "basic": {
        "text": "Basic Subscription",
        "rect": pygame.Rect(120, 350, 300, 60),
        "color": (180, 80, 80),
        "clicked": False,
        "price": "5$"
    },
    "family": {
        "text": "Family Subscription",
        "rect": pygame.Rect(120, 430, 300, 60),
        "color": (180, 80, 80),
        "clicked": False,
        "price": "8$"
    }
}

free_button_rect = pygame.Rect(80, 700, 380, 30)
free_button_clicked = False

music_list = [
    {
        "text": "Audioslave - Be Yourself",
        "photo": pygame.image.load(album_audio).convert_alpha(),
        "color": (57, 60, 77),
        "music": pygame.mixer.Sound(os.path.join("музыка", "be yourself.mp3"))
    },
    {
        "text": "30 Seconds to Mars - The Kill",
        "photo": pygame.image.load(album_mars).convert_alpha(),
        "color": (247, 104, 104),
        "music": pygame.mixer.Sound(os.path.join("музыка", "kill.mp3"))
    },
    {
        "text": "Creed - One Last Breath",
        "photo": pygame.image.load(album_creed).convert_alpha(),
        "color": (138, 128, 73),
        "music": pygame.mixer.Sound(os.path.join("музыка", "one last breath.mp3"))
    }
]

current_song = 0
music_playing = False

play_button_rect = pygame.Rect(WIDTH // 2 - 40, HEIGHT - 150, 80, 80)
next_button_rect = pygame.Rect(WIDTH - 100, HEIGHT - 130, 80, 40)
back_button_rect = pygame.Rect(30, HEIGHT - 130, 80, 40)
playlist_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 60)


avatar_size = 50
animation_time = 60
frame = 0
start.play()

ad_images = [
    pygame.image.load(os.path.join("фото", "реклама1.png")).convert_alpha(),
    pygame.image.load(os.path.join("фото", "реклама2.png")).convert_alpha(),
    pygame.image.load(os.path.join("фото", "реклама3.png")).convert_alpha(),
]
ad_clicked = False
ad_c = 0
cross_size = 30  
ad_x = WIDTH - 20  
ad_y = HEIGHT - 200  

cross_x = ad_x - cross_size  
cross_y = ad_y + 10  
cross_rect = pygame.Rect(cross_x, cross_y, cross_size, cross_size)

while True: 

    screen.fill(BG_COLOR if state != "music" else music_list[current_song]["color"])

    mouse_pos = pygame.mouse.get_pos()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == "subscription":
                for button_key in subscription_buttons:
                    button = subscription_buttons[button_key]
                    if button["rect"].collidepoint(event.pos):
                        button["clicked"] = True
                        if button_key == "family":
                            pygame.quit()
                            sys.exit()

                if free_button_rect.collidepoint(event.pos):
                    free_button_clicked = True


    if state == "animation":
        avatar_size = min(300, 50 + (frame * 5))
        avatar_scaled = pygame.transform.smoothscale(avatar, (avatar_size, avatar_size))
        screen.blit(avatar_scaled, (WIDTH // 2 - avatar_size // 2, HEIGHT // 2 - avatar_size // 2))
        frame += 1
        if frame >= animation_time:
            state = "subscription"

    elif state == "subscription":
        font_title = pygame.font.Font(None, 80)
        Subscribe_button = font_title.render("Subscribe", True, TEXT_COLOR)
        screen.blit(Subscribe_button, (WIDTH // 2 -  Subscribe_button.get_width() // 2, 50))

        font_button = pygame.font.Font(None, 40)
        font_price = pygame.font.Font(None, 30)  
        mouse_pos = pygame.mouse.get_pos()

        for button_key in subscription_buttons:
            button = subscription_buttons[button_key]
            color = button["color"]

            if button["rect"].collidepoint(mouse_pos) and not button["clicked"]:
                color = BUTTON_HOVER
                
                price_surf = font_price.render(button["price"], True, TEXT_COLOR)
                screen.blit(price_surf, (button["rect"].right + 10, button["rect"].centery - 10))

            if button["clicked"]:
                    overlay = pygame.Surface((button["rect"].width, button["rect"].height), pygame.SRCALPHA)
                    pygame.draw.rect(overlay, (255, 255, 255, 70), overlay.get_rect(), border_radius=10)
                    screen.blit(overlay, button["rect"])

                    pygame.display.flip()
                    pygame.time.delay(30) 

                    button["clicked"] = False  

                    if button_key == "family":
                        pygame.quit()
                        sys.exit()  
            
            pygame.draw.rect(screen, color, button["rect"], border_radius=10)
            text_surf = font_button.render(button["text"], True, TEXT_COLOR)
            screen.blit(text_surf, (button["rect"].x + 20, button["rect"].y + 15))


        font_free = pygame.font.Font(None, 30)
        free_text = "No, I'll continue with the free version"
        free_surf = font_free.render(free_text, True, TEXT_COLOR)
        pygame.draw.rect(screen, BUTTON_COLOR, free_button_rect, border_radius=5)
        screen.blit(free_surf, (free_button_rect.x + 10, free_button_rect.y + 5))

        if free_button_clicked:
            state = "main"

    elif state == "main":

        font_main = pygame.font.Font(None, 60)
        main_text = font_main.render("Divorced Father Music", True, TEXT_COLOR)
        screen.blit(main_text, (WIDTH // 2 - main_text.get_width() // 2, 100))
    
        pygame.draw.rect(screen, BUTTON_DEFAULT, playlist_button, border_radius=10)
        font_playlist = pygame.font.Font(None, 40)
        text_playlist = font_playlist.render("Play Free Playlist", True, TEXT_COLOR)
        screen.blit(text_playlist, (playlist_button.x + 20, playlist_button.y + 15))

        if event.type == pygame.MOUSEBUTTONDOWN and playlist_button.collidepoint(event.pos):
            state = "music"

        screen.blit(ad_images[ad_c], (WIDTH // 2 - ad_images[ad_c].get_width() // 2, 630))
        if event.type == pygame.MOUSEBUTTONDOWN and not ad_clicked:
            if cross_rect.collidepoint(event.pos):
                ad_clicked = True  
                ad_c = (ad_c + 1) % len(ad_images)
        if event.type == pygame.MOUSEBUTTONUP:
            ad_clicked = False  
                

    elif state == "music":
        current_time = pygame.time.get_ticks()
    
        if girl_timer is None:  
            girl_timer = current_time  
        album_art = pygame.transform.scale(music_list[current_song]["photo"], (300, 300))
        screen.blit(album_art, (WIDTH // 2 - 150, HEIGHT // 2 - 200))
        font_song = pygame.font.Font(None, 40)
        song_text = font_song.render(music_list[current_song]["text"], True, TEXT_COLOR)
        screen.blit(song_text, (WIDTH // 2 - song_text.get_width() // 2, HEIGHT // 2 + 120))
        
        screen.blit(play_icon if not music_playing else pause_icon, (play_button_rect.x + 15, play_button_rect.y + 10))

        if event.type == pygame.MOUSEBUTTONDOWN and not check and not check_2:
            if play_button_rect.collidepoint(event.pos):
                music_playing = not music_playing
                check = True
                if music_playing:
                    music_list[current_song]["music"].play()
                else:
                    music_list[current_song]["music"].stop()
                    
            if next_button_rect.collidepoint(event.pos):
                music_playing = False
                music_list[current_song]["music"].stop()
                current_song = (current_song + 1) % len(music_list)
                check_2 = True

            if back_button_rect.collidepoint(event.pos):
                state = "main"  
                music_playing = not music_playing
                music_list[current_song]["music"].stop()
                girl_timer = None  
                girl = False  
        if event.type == pygame.MOUSEBUTTONUP:
            check = False
            check_2 = False
        font_next = pygame.font.Font(None, 30)
        next_text = font_next.render("Next", True, TEXT_COLOR)
        pygame.draw.rect(screen, (50, 50, 50), next_button_rect, border_radius=10)
        screen.blit(next_text, (next_button_rect.x + 20, next_button_rect.y + 10))

        font_next = pygame.font.Font(None, 30)
        back_text = font_next.render("Back", True, TEXT_COLOR)
        pygame.draw.rect(screen, (50, 50, 50), back_button_rect, border_radius=10)
        screen.blit(back_text, (back_button_rect.x + 20, back_button_rect.y + 10))

        if girl_timer and current_time - girl_timer > 5000:
            Vision = False
            girl = not girl
            if girl:
                girl_c = (girl_c + 1) % len(girl_images)
                girlsound.play()
                Vision = True
            girl_timer = current_time     
    
        if Vision:
            screen.blit(girl_images[girl_c], (girl_x,girl_y))
            

    pygame.display.flip()
    clock.tick(60)
