import pygame
import random
import time
import pygame.mixer
import sys

pygame.init()
pygame.mixer.init()

FPS = 60
DOT_RADIUS = 30
DOT_COLOR = (227, 116, 160)
BACKGROUND_COLOR = (40, 40, 40)
ROUND_TIME_LIMIT = 120
DISPLAY_TIME = 5
TEXT_COLOR = (255, 255, 255)
TRAIL_LENGTH = 20  # Довжина сліду
TRAIL_COLOR = (150, 150, 150)
PROBABILITY_DOT = 0.8 #80% (шанс випадіння)
PROBABILITY_KEY = 0.2 
KEY_COLOR = (212, 124, 252)
CURSOR_SIZE = (32, 32)
MUSIK_VOLUME = 0.15

BUTTON_WIDTH = 400
BUTTON_HEIGHT = 80
BORDER_RADIUS = 10
BUTTON_COLOR = (227, 206, 20)
BUTTON_HOVER_COLOR = (187, 166, 20)

screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("DOS")

clock = pygame.time.Clock()
clock.tick(FPS)

ani_cursor = pygame.image.load("resource/image/pointer.png")
ani_cursor = pygame.transform.scale(ani_cursor, CURSOR_SIZE)
pygame.mouse.set_visible(False)


def display_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def draw_button(rect, color):
    pygame.draw.rect(screen, color, rect, border_radius=BORDER_RADIUS)

def game():
    running = True
    background_image = pygame.image.load("resource/image/fon.jpg").convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    background_sound = pygame.mixer.Sound("resource/sound/background_sound.wav")

    background_sound.set_volume(MUSIK_VOLUME)
    background_sound.play()

    def play(running):
        pause = False
        start_time = time.time()
        total_hits = 0
        missclick = 0
        point_appeared = False
        point_x, point_y = 0, 0
        point_time = time.time()
        cursor_trail = []  # Список для збереження попередніх позицій курсора
        target_key = ""
        selected = ""
        click_sound = pygame.mixer.Sound("resource/sound/click.wav")
        chik_sound = pygame.mixer.Sound("resource/sound/chik.wav")
        timer_sound = pygame.mixer.Sound("resource/sound/timer.wav")
        
        while running:
            current_time = time.time()
            elapsed_time = current_time - start_time
            point_elapsed_time = current_time - point_time

            def random_word():
                chance = random.randint(0, 99)
                if chance <= 79:
                    return "DOT"
                else:
                    return "KEY"
            
            if not pause and elapsed_time <= 3:
                # screen.fill(BACKGROUND_COLOR)
                screen.blit(background_image, (0, 0))
                if elapsed_time <= 1:
                    timer_sound.set_volume(MUSIK_VOLUME)
                    timer_sound.play()
                    display_text("3", 80, (255, 255, 255), WIDTH // 2, (HEIGHT // 2))
                elif elapsed_time <= 2:
                    timer_sound.set_volume(MUSIK_VOLUME)
                    timer_sound.play()
                    display_text("2", 80, (255, 255, 255), WIDTH // 2, (HEIGHT // 2))
                elif elapsed_time <= 3:
                    timer_sound.set_volume(MUSIK_VOLUME)
                    timer_sound.play()
                    display_text("1", 80, (255, 255, 255), WIDTH // 2, (HEIGHT // 2))
            elif not pause:
                # screen.fill(BACKGROUND_COLOR)
                screen.blit(background_image, (0, 0))
                elapsed_time -= 3

                mouse_x, mouse_y = pygame.mouse.get_pos()
                cursor_trail.append((mouse_x, mouse_y))  # Додаємо поточні координати курсора до списку
                if len(cursor_trail) > TRAIL_LENGTH:  # Зберігаємо тільки останні TRAIL_LENGTH позицій
                    cursor_trail.pop(0)
                # Малюємо лінії від останньої позиції до попередніх
                for i in range(1, len(cursor_trail)):
                    pygame.draw.line(screen, TRAIL_COLOR, cursor_trail[i - 1], cursor_trail[i], 4)


                if elapsed_time >= ROUND_TIME_LIMIT:
                    pause = True
                    stop_time = elapsed_time

                if selected == "":
                    selected = random_word()
                    # print(selected)

                if not point_appeared and point_elapsed_time < DISPLAY_TIME and selected == "DOT":
                    point_x, point_y = random.randint(DOT_RADIUS, WIDTH - DOT_RADIUS), random.randint(DOT_RADIUS, HEIGHT - DOT_RADIUS)
                    point_appeared = True
                    point_time = time.time()

                if point_appeared and selected == "DOT":
                    pygame.draw.circle(screen, DOT_COLOR, (point_x, point_y), DOT_RADIUS)

                if point_elapsed_time >= DISPLAY_TIME and selected == "DOT":
                    point_appeared = False
                    selected = ""
                    point_time = time.time()

                if not point_appeared and point_elapsed_time < DISPLAY_TIME and selected == "KEY":
                    if random.random() < PROBABILITY_KEY:
                        point_x, point_y = random.randint(DOT_RADIUS, WIDTH - DOT_RADIUS), random.randint(DOT_RADIUS, HEIGHT - DOT_RADIUS)
                        target_key = random.choice("WASDQERFGTCVBNM12345")  # Додай бажані символи
                        point_appeared = True
                        point_time = time.time()


                if point_appeared and selected == "KEY":
                    pygame.draw.circle(screen, KEY_COLOR, (point_x, point_y), DOT_RADIUS)
                    display_text(target_key, 30, TEXT_COLOR, point_x, point_y)


                if point_elapsed_time >= DISPLAY_TIME and selected == "KEY":
                    point_appeared = False
                    point_time = time.time()
                    selected = ""
                

                display_text("Час: {:.2f} сек.".format(elapsed_time), 30, (255, 255, 255), WIDTH // 14, 50)
                display_text("Влучень: {}".format(total_hits), 30, (255, 255, 255), WIDTH // 14, 80)
                display_text("Помилкових натискань: {}".format(missclick), 30, (255, 255, 255), WIDTH // 14, 110)
            else: #підсумки
                # screen.fill(BACKGROUND_COLOR)
                screen.blit(background_image, (0, 0))
                display_text("Підсумки!", 30, (255, 255, 255), WIDTH // 2, ((HEIGHT // 2)-60))
                display_text("Час: {:.2f} сек.".format(stop_time), 30, (255, 255, 255), WIDTH // 2, ((HEIGHT // 2)-30))
                display_text("Влучень: {}".format(total_hits), 30, (255, 255, 255), WIDTH // 2, (HEIGHT // 2))
                display_text("Помилкових натискань: {}".format(missclick), 30, (255, 255, 255), WIDTH // 2, ((HEIGHT // 2)+30))

            pos = pygame.mouse.get_pos()
            screen.blit(ani_cursor, pos)

            pygame.display.flip() # оновлює зображення
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif not pause and point_appeared:
                        pressed_key = pygame.key.name(event.key)
                        if pressed_key.upper() == target_key and selected == "KEY":
                            print("Точка натискана! Витрачено часу: {:.2f} сек.".format(elapsed_time))
                            total_hits += 1
                            point_appeared = False
                            point_time = time.time()
                            selected = ""
                            chik_sound.play()
                        else:
                            missclick += 1
                            click_sound.play()
                elif event.type == pygame.MOUSEBUTTONDOWN and not pause: 
                    mouse_x, mouse_y = event.pos
                    distance = ((mouse_x - point_x) ** 2 + (mouse_y - point_y) ** 2) ** 0.5
                    if distance < DOT_RADIUS and point_appeared  and selected == "DOT":
                        # print("Точка натискана! Витрачено часу: {:.2f} сек.".format(elapsed_time))
                        total_hits += 1
                        point_appeared = False
                        point_time = time.time()
                        selected = ""
                        chik_sound.play()
                    else:
                        missclick += 1
                        click_sound.play()
    while running:
        middle_width = (WIDTH - BUTTON_WIDTH) // 2
        middle_hight = (HEIGHT - BUTTON_HEIGHT) // 2
        screen.blit(background_image, (0, 0))

        play_button = pygame.Rect(middle_width, (middle_hight-120), BUTTON_WIDTH, BUTTON_HEIGHT)
        if play_button.collidepoint(pygame.mouse.get_pos()):
            draw_button(play_button, BUTTON_HOVER_COLOR)
        else:
            draw_button(play_button, BUTTON_COLOR)
        display_text("Грати", 30, TEXT_COLOR, middle_width+190, (middle_hight-80))

        settings_button = pygame.Rect(middle_width, middle_hight, BUTTON_WIDTH, BUTTON_HEIGHT)
        if settings_button.collidepoint(pygame.mouse.get_pos()):
            draw_button(settings_button, BUTTON_HOVER_COLOR)
        else:
            draw_button(settings_button, BUTTON_COLOR)
        display_text("Налаштування", 30, TEXT_COLOR, middle_width+195, middle_hight+40)
        

        quit_button = pygame.Rect(middle_width, (middle_hight+120), BUTTON_WIDTH, BUTTON_HEIGHT)
        if quit_button.collidepoint(pygame.mouse.get_pos()):
            draw_button(quit_button, BUTTON_HOVER_COLOR)
        else:
            draw_button(quit_button, BUTTON_COLOR)
        display_text("Вийти", 30, TEXT_COLOR, middle_width+190,(middle_hight+160))


        pos = pygame.mouse.get_pos()
        screen.blit(ani_cursor, pos)
        pygame.display.flip()
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.collidepoint(event.pos):
                        play(running)
                    elif settings_button.collidepoint(event.pos):
                        print("settings")
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()


game()
