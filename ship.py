import pygame
import math

class Ship:
    def __init__(self, position=(0, 0), speed=100, turn_speed=300):
        self.position = pygame.Vector2(position)
        self.speed = speed  # This is now the forward speed
        self.turn_speed = turn_speed  # Turning speed
        self.direction = pygame.Vector2(0, -1)  # Default facing up
        self.angle = 0  # Ship's current angle in degrees
        self.min_speed = 0.1  # Minimum speed the ship can go

    def turn(self, angle_change):
        """Turns the ship without changing its position."""
        self.angle += angle_change
        self.angle %= 360  # Keep the angle within 0-360 degrees

    def move_forward(self, dt):
        """Moves the ship forward based on its current direction."""
        rad_angle = math.radians(self.angle)
        self.position += pygame.Vector2(math.cos(rad_angle), math.sin(rad_angle)) * self.speed * dt

    def adjust_speed(self, adjustment):
        """Adjusts the ship's speed while ensuring it doesn't fall below the min_speed."""
        # Adjust the speed with the given adjustment
        self.speed += adjustment

        # If after adjustment, speed is less than min_speed, set it to min_speed
        if self.speed < self.min_speed:
            self.speed = self.min_speed
        # You might also want to put an upper limit on speed if necessary

    def get_velocity_vector(self):
        """Returns the velocity vector of the ship based on its speed and direction."""
        rad_angle = math.radians(self.angle)
        direction_vector = pygame.Vector2(math.cos(rad_angle), math.sin(rad_angle))
        velocity_vector = direction_vector * self.speed
        return velocity_vector

