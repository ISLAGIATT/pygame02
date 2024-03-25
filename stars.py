import pygame
import random

class Star:
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = random.randrange(0, screen_width)
        self.y = random.randrange(0, screen_height)
        self.z = random.randrange(1, screen_width)
        self.speed = random.random() * 2 + 0.1

    def update(self):
        self.z -= self.speed
        if self.z <= 0:
            self.x = random.randrange(0, self.screen_width)
            self.y = random.randrange(0, self.screen_height)
            self.z = self.screen_width
            self.speed = random.random() * 2 + 0.1

    def draw(self, screen):
        epsilon = 0.1  # Small value to prevent division by zero
        x, y = (
        (self.x - self.screen_width // 2) / ((self.z + epsilon) / (self.screen_width // 2)) + self.screen_width // 2,
        (self.y - self.screen_height // 2) / ((self.z + epsilon) / (self.screen_width // 2)) + self.screen_height // 2)
        radius = max(1,
                     (self.screen_width - self.z) / self.screen_width)  # Ensure radius is at least 1 to draw the star
        pygame.draw.circle(screen, self.WHITE, (int(x), int(y)), int(radius))

class Comet:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = random.randrange(screen_width, screen_width + 100)  # Start off-screen
        self.y = random.randrange(0, screen_height)
        self.size = random.randrange(1, 3)
        self.velocity = random.random() * 2 + 1  # Adjust speed as needed

    def update(self):
        self.x -= self.velocity  # Move left across the screen
        # You can add more complex motion or fading here

    def draw(self, screen):
        # For a simple comet, draw a circle and potentially a line for the tail
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.size)
        # Add tail
        tail_length = 3  # Adjust as necessary for visibility
        tail_width = 3  # Make the tail thicker for visibility
        pygame.draw.line(screen, (255, 255, 255), (int(self.x), int(self.y)), (int(self.x) + tail_length, int(self.y)),
                         tail_width)

