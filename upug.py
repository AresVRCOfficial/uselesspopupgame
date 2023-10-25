import pygame
import sys
import random
import os
from pypresence import Presence

pygame.init()

# Get display dimensions
WIDTH, HEIGHT = 800, 600

win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("\033[48;2;255;0;0m Useless Pop-up Box \033[0m")

# Fonts
font = pygame.font.Font(None, 36)
wacky_font = pygame.font.Font(None, 72)

# Game variables
points = 0
target_points = 1000
movement_speed = 5

# State variables
state = "start"  # Possible states: "start", "game", "credits"

# Box position variables
box_x, box_y = WIDTH // 2 - 100, HEIGHT // 2 - 50  # Initial position of the box

# Particle variables
particles = []
for _ in range(200):
    particle_size = random.randint(5, 15)
    particle_x = random.randint(0, WIDTH)
    particle_y = random.randint(0, HEIGHT)
    particle_speed_x = random.randint(-2, 2)
    particle_speed_y = random.randint(-2, 2)
    # Generate random RGB values for particle color
    particle_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    particles.append([particle_x, particle_y, particle_size, particle_speed_x, particle_speed_y, particle_color])

# Load sounds
button_pressed_sound = pygame.mixer.Sound(os.path.join("sounds", "button_pressed.wav"))
level_up_sound = pygame.mixer.Sound(os.path.join("sounds", "level-up.wav"))

# Load background music
pygame.mixer.music.load(os.path.join("sounds", "soundtrack.mp3"))

# Play background music in a loop
pygame.mixer.music.play(-1)

# Initialize Discord Rich Presence client
client_id = '1166591107103195207'
RPC = Presence(client_id)
RPC.connect()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RPC.close()  # Disconnect Discord Rich Presence client before quitting
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            # Handle window resize event
            WIDTH, HEIGHT = event.w, event.h
            win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if state == "start":
                # Check if play button is clicked
                play_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2, 100, 50)
                credits_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 70, 100, 50)
                if play_button_rect.collidepoint(event.pos):
                    state = "game"
                elif credits_button_rect.collidepoint(event.pos):
                    state = "credits"
            elif state == "game":
                # Check if the box is clicked
                if box_x < mouse_x < box_x + 200 and box_y < mouse_y < box_y + 100:
                    points += 1
                    button_pressed_sound.play()  # Play button pressed sound
                    if points >= target_points:
                        print("You win!")
                        pygame.quit()
                        sys.exit()
                    # Reset box position to a random location in the window
                    box_x = random.randint(0, WIDTH - 200)
                    box_y = random.randint(0, HEIGHT - 100)
                    movement_speed += 1
            elif state == "credits":
                # Check if back button is clicked
                back_button_rect = pygame.Rect(20, HEIGHT - 70, 100, 50)
                if back_button_rect.collidepoint(event.pos):
                    state = "start"

    # Get current mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Clear the screen
    win.fill((0, 0, 0))  # Set the window background color to black

    # Draw particles
    for particle in particles:
        particle[0] += particle[3]  # Move particle horizontally
        particle[1] += particle[4]  # Move particle vertically
        # Wrap particles around the screen if they go out of bounds
        particle[0] %= WIDTH
        particle[1] %= HEIGHT
        pygame.draw.circle(win, particle[5], (particle[0], particle[1]), particle[2])

    # Update Discord Rich Presence status
    RPC.update(
        state='Playing Useless Pop Up Game by Mistress Ares',
        details=f'Points: {points}',
        large_image='large_image_key',  # Replace 'large_image_key' with your large image key
        large_text='Useless Pop-up Madness'  # Replace 'Useless Pop-up Madness' with your large image text
    )

    if state == "start":
        # Draw start screen
        title_text = wacky_font.render("Useless Pop-up Madness", True, (255, 255, 255))
        play_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2, 100, 50)
        credits_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 70, 100, 50)
        pygame.draw.rect(win, (0, 255, 0), play_button_rect)
        pygame.draw.rect(win, (0, 255, 0), credits_button_rect)
        play_text = font.render("Play", True, (0, 0, 0))
        credits_text = font.render("Credits", True, (0, 0, 0))
        win.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 200))
        win.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, HEIGHT // 2 + 10))
        win.blit(credits_text, (WIDTH // 2 - credits_text.get_width() // 2, HEIGHT // 2 + 80))

    elif state == "game":
        # Draw the pop-up box
        pygame.draw.rect(win, (255, 0, 0), (box_x, box_y, 200, 100))
        points_text = font.render(f"Points: {points}", True, (255, 255, 255))
        win.blit(points_text, (10, 10))

        # Level up the player every 100 points
        if points % 100 == 0 and points > 0:
            level_up_sound.play()  # Play level up sound
            movement_speed += 1  # Increase movement speed
            # ... (you can add more actions for level up if desired)

    elif state == "credits":
        # Draw credits screen
        credits_text = font.render("Game by: Mistress Ares", True, (255, 255, 255))
        pygame.draw.rect(win, (0, 255, 0), pygame.Rect(20, HEIGHT - 70, 100, 50))
        back_text = font.render("Back", True, (0, 0, 0))
        win.blit(credits_text, (WIDTH // 2 - credits_text.get_width() // 2, HEIGHT // 2 - 50))
        win.blit(back_text, (30, HEIGHT - 60))

    # Update the display
    pygame.display.flip()




