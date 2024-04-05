import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 2560
screen_height = 1440
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Font Examples")

# Define fonts to display (For demonstration, this will get all available fonts)
fonts_to_display = pygame.font.get_fonts()

# Colors
bg_color = (30, 30, 30)
text_color = (255, 255, 255)

# Font settings
font_size = 18  # Adjust based on your preference and screen size
max_fonts_per_col = screen_height // (font_size + 10)  # Calculate how many fonts fit per column

def draw_fonts(screen, fonts):
    screen.fill(bg_color)
    column_width = screen_width // (len(fonts) // max_fonts_per_col + 1)  # Calculate column width
    x, y = 10, 10  # Starting position

    for font_name in fonts:
        try:
            font = pygame.font.SysFont(font_name, font_size)
            text_surface = font.render(f"{font_name}", True, text_color)
            screen.blit(text_surface, (x, y))
            y += font_size + 10  # Move down to the next line
            if y + font_size > screen_height:  # Check if we've reached the bottom of the screen
                y = 10  # Reset Y
                x += column_width  # Move to the next column
        except Exception as e:
            print(f"Error displaying font '{font_name}': {e}")

    pygame.display.flip()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_fonts(screen, fonts_to_display)

pygame.quit()
sys.exit()
