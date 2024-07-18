import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tokecon")

# Load background image and scale it to fit the screen
background_image = pygame.image.load('Assets/MenuBackground2.jpeg').convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Custom font file path
font_path = "Assets/ThaleahFat.ttf"

# Fonts
title_font = pygame.font.Font(font_path, 48)  # You can specify a font file or use None for default font
menu_font = pygame.font.Font(font_path, 36)

# Menu options
menu_options = ["Play", "Set Bounties", "Settings"]
selected_option = 0

# Function to render text centered horizontally
# Function to render text centered horizontally with outline
def draw_text(text, font, color, outline_color, surface, x, y):
    # Render text with black outline
    text_render = font.render(text, True, outline_color)
    text_rect = text_render.get_rect()
    text_rect.center = (x + 2, y + 2)  # Offset for outline
    surface.blit(text_render, text_rect)

    # Render text in desired color
    text_render = font.render(text, True, color)
    text_rect = text_render.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_render, text_rect)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_option = (selected_option - 1) % len(menu_options)
            elif event.key == pygame.K_DOWN:
                selected_option = (selected_option + 1) % len(menu_options)
            elif event.key == pygame.K_RETURN:
                if selected_option == 0:
                    print("Play selected")
                    # Implement play action
                elif selected_option == 1:
                    print("Set Bounties selected")
                    # Implement set bounties action
                elif selected_option == 2:
                    print("Settings selected")
                    # Implement settings action

    # Clear the screen
    screen.blit(background_image, (0, 0))

    # Draw title
    draw_text("Your Game Title", title_font, pygame.Color('white'), pygame.Color('black'), screen, SCREEN_WIDTH // 2, 100)

    # Draw menu options
    for i, option in enumerate(menu_options):
        if i == selected_option:
            draw_text(option, menu_font, pygame.Color('yellow'), pygame.Color('black'), screen, SCREEN_WIDTH // 2, 300 + i * 50)
        else:
            draw_text(option, menu_font, pygame.Color('white'), pygame.Color('black'), screen, SCREEN_WIDTH // 2, 300 + i * 50)

    pygame.display.flip()  # Update the display

pygame.quit()
sys.exit()
