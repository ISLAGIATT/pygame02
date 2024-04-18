import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Sprite Sheet Animation")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Load the sprite sheet
sprite_sheet_image = pygame.image.load('images/PlayerWalk 48x48.png').convert_alpha()

def get_image(x, y, width, height):
    """Extracts a single image from a sprite sheet at x, y with the specified width and height."""
    image = pygame.Surface((width, height), pygame.SRCALPHA)
    image.blit(sprite_sheet_image, (0, 0), (x, y, width, height))
    return image

frame_width = 48
frame_height = 48
frames = []
num_frames = 8  # Number of frames in the sprite sheet
# Initialize frame variables
frame_count = 0
current_frame = 0

for i in range(num_frames):
    frame = get_image(i * frame_width, 0, frame_width, frame_height)
    frames.append(frame)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update frame based on your frame count or timer
    frame_count += 1
    if frame_count >= 6:  # Change the frame every 6 ticks
        current_frame = (current_frame + 1) % num_frames
        frame_count = 0

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw the current frame
    screen.blit(frames[current_frame], (100, 100))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()