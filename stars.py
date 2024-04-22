import pygame
import pygame.sprite
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
        self.z = random.uniform(0.02, 1.0)  # z represents depth, and should never be 0

    def update(self, ship_velocity_vector, dt):
        # Simulate star moving towards the player by decreasing z
        self.z -= ship_velocity_vector.length() * dt * 0.1  # Scale the effect based on ship's speed
        if self.z <= 0:
            self.reset_star()

    def draw(self, screen):
        # 3D scaling effect
        x_center, y_center = self.screen_width / 2, self.screen_height / 2
        scale = 200  # size of stars
        x_2d = (self.x / self.z) * scale + x_center
        y_2d = (self.y / self.z) * scale + y_center

        # Draw stars (circles) here
        radius = max(1, 2 * (1 - self.z))
        if abs(x_2d) < 10000 and abs(y_2d) < 10000:  # Arbitrary large value check so it dont crash
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

class Planetoid(pygame.sprite.Sprite):
    def __init__(self, image_path, position, object_id, initial_scale=1.0, scaling_rate=0.0005, orbit_speed=5, max_scale=2.0):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.position = pygame.Vector2(position)
        self.scale_factor = initial_scale
        self.scaling_rate = scaling_rate
        self.orbit_speed = orbit_speed
        self.max_scale = max_scale
        self.update_image()
        self.behind_player = False
        self.is_visible = True
        self.object_id = object_id
        self.comms_distance = False  # close enough for comms?

    def update_image(self):
        # Apply scaling to the planetoid image
        scaled_width = int(self.original_image.get_width() * self.scale_factor)
        scaled_height = int(self.original_image.get_height() * self.scale_factor)
        self.image = pygame.transform.scale(self.original_image, (scaled_width, scaled_height))
        self.rect = self.image.get_rect(center=self.position)

    def update(self, dt, ship_yaw_change, ship_pitch_change, ship_speed, screen_center):
        # Calculate the distance from the planetoid to the screen center
        distance_to_center = self.position.distance_to(screen_center)

        # Normalize the distance based on screen size for consistent behavior on different resolutions
        max_distance = (screen_center.x ** 2 + screen_center.y ** 2) ** 0.5
        normalized_distance = distance_to_center / max_distance

        # Adjust the scaling rate based on how close the object is to the screen's center
        adjusted_scaling_rate = self.scaling_rate * (1 - normalized_distance) ** 2  # Quadratic falloff

        # things get closer when you face them. get further when behind you
        if not self.behind_player:
            self.scale_factor += ship_speed * dt * adjusted_scaling_rate
        else:
            self.scale_factor -= ship_speed * dt * adjusted_scaling_rate

        # Clamp the scale factor using the max_scale value
        self.scale_factor = max(0.1, min(self.scale_factor, self.max_scale))

        # Check if scale_factor of space_station_01 reaches 0.75
        if self.object_id == "space_station_01" and self.scale_factor >= 0.75 and not self.comms_distance:
            self.comms_distance = True


        self.update_image()
