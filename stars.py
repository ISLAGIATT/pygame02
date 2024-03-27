import pygame
import random
import math

class Star:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.reset_star()

    def reset_star(self):
        # Stars are initially placed with random x, y values and a z value that simulates depth
        self.x = random.uniform(-1, 1)
        self.y = random.uniform(-1, 1)
        self.z = random.uniform(0.01, 1.0)  # z represents depth, and should never be 0

    def update(self, ship_velocity_vector, dt):
        # Simulate star moving towards the player by decreasing z
        self.z -= ship_velocity_vector.length() * dt * 0.1  # Scale the effect based on ship's speed
        if self.z <= 0:
            self.reset_star()

    def draw(self, screen):
        # Convert 3D star position to 2D using perspective projection
        x_center, y_center = self.screen_width / 2, self.screen_height / 2
        scale = 200  # Adjust scale to control how large the stars appear based on depth
        x_2d = (self.x / self.z) * scale + x_center
        y_2d = (self.y / self.z) * scale + y_center

        # Draw the star as a circle, with size based on depth
        radius = max(1, 2 * (1 - self.z))
        pygame.draw.circle(screen, (255, 255, 255), (int(x_2d), int(y_2d)), radius)

class Comet:
    WHITE = (255, 255, 255)
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.reset_comet()

    def reset_comet(self):
        self.x = random.randrange(self.screen_width, self.screen_width + 100)
        self.y = random.randrange(0, self.screen_height)
        self.size = random.randrange(1, 3)
        self.velocity = random.random() * 2 + 1

    def update(self, ship_yaw, ship_pitch, dt):
        self.x -= (self.velocity + ship_yaw * dt * 50)  # Consider ship's yaw effect
        self.y += ship_pitch * dt * 50  # Consider ship's pitch effect

        if self.x < -100 or self.x > self.screen_width + 100 or self.y < -100 or self.y > self.screen_height + 100:
            self.reset_comet()

    def draw(self, screen):
        tail_length = 10
        tail_width = 2
        pygame.draw.circle(screen, self.WHITE, (int(self.x), int(self.y)), self.size)
        pygame.draw.line(screen, self.WHITE, (int(self.x), int(self.y)), (int(self.x) + tail_length, int(self.y)), tail_width)

class Planetoid:
    def __init__(self, image_path, position, initial_scale=1.0):
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.position = pygame.Vector2(position)
        self.scale_factor = initial_scale
        self.update_image()

    def update_image(self):
        # Apply the new scale to the planetoid image
        scaled_width = int(self.original_image.get_width() * self.scale_factor)
        scaled_height = int(self.original_image.get_height() * self.scale_factor)
        self.image = pygame.transform.scale(self.original_image, (scaled_width, scaled_height))
        self.rect = self.image.get_rect(center=self.position)

    def update(self, dt, ship_yaw_change, ship_pitch_change, ship_speed):
        # Scale the planetoid based on the ship's forward speed
        # velocity_magnitude = ship_velocity_vector.length()
        # Adjust scale factor based on speed; more speed = larger scale change
        # The 0.0005 multiplier is an arbitrary scale factor for how quickly the planetoid scales based on speed
        self.scale_factor += ship_speed * dt * 0.0005

        # Clamp the scale factor to prevent it from going below or above desired thresholds
        self.scale_factor = max(0.1, min(self.scale_factor, 5.0))

        self.update_image()

        # Adjust position based on ship's yaw and pitch changes
        self.position.x += ship_yaw_change * dt * -10  # Adjust direction based on yaw
        self.position.y += ship_pitch_change * dt * 10  # Adjust direction based on pitch

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)