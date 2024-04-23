import pygame
import pygame.sprite
import random
import time

from game_state_manager import GameStateManager
from mouse_event import MouseEventHandler
from stars import Star, Comet, Planetoid

mouse_event_handler = MouseEventHandler
game_state_manager = GameStateManager
class LandingScene:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.run = True
        #self.mouse_event_handler = MouseEventHandler()

        # Load images and setup positions
        self.spaceport_img = pygame.image.load('images/space_station_landing01.png')
        self.spaceport_rect = self.spaceport_img.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        self.original_ship_img = pygame.image.load('images/ship_landing.png')
        self.ship_rect = self.original_ship_img.get_rect(
            center=(screen.get_width() // 2, -self.original_ship_img.get_height()))
        self.landing_x = 559
        self.landing_y = 870
        self.landing_speed = 175  # Define landing speed here
        self.scaling_rate = .001
        self.ship_img = None

        self.person_sprite_sheet_image = pygame.image.load('images/PlayerWalk 48x48.png').convert_alpha()
        self.delay_start_time = None

        self.person_frames = [self.get_person_image(i * 48, 0, 48, 48) for i in range(8)]
        self.person_current_frame = 0
        self.person_frame_count = 0
        self.person_position = [self.ship_rect.centerx, self.ship_rect.bottom]
        self.person_walking_speed = 150
        self.person_visible = False
        self.person_walking = False

        self.stars = [Star(screen.get_width(), screen.get_height()) for _ in range(300)]
        self.comets = []
        self.planetoids = pygame.sprite.LayeredUpdates()
        self.setup_planetoids()

        self.current_scale = 1.0
        self.zoom_out_rate = 0.99  # Adjust the rate as needed
        self.zoom_out = False

        pygame.mixer.music.load("./music/Ancient-Game-Menu.ogg")
        pygame.mixer.music.set_volume(0.50)
        pygame.mixer.music.play(loops=-1)

    def get_person_image(self, x, y, width, height):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.person_sprite_sheet_image, (0, 0), (x, y, width, height))
        return image

    def setup_planetoids(self):
        planetoid_01 = Planetoid('images/green_planet01.png', (300, 300), "planetoid_01", initial_scale=0.30,
                                 scaling_rate=.00005, orbit_speed=1)
        star_01 = Planetoid('images/star01.png', (400, 400), "star_01", initial_scale=.2, scaling_rate=0,
                            orbit_speed=.25)
        self.planetoids.add(star_01, layer=0)
        self.planetoids.add(planetoid_01, layer=1)

    def update(self, dt):
        # Calculate distance to landing zone
        distance_to_landing = self.landing_y - self.ship_rect.centery

        # Slow down as it approaches landing
        if distance_to_landing < 200:
            self.landing_speed = 100

        # Move ship towards landing zone
        if self.ship_rect.centery < self.landing_y:
            self.ship_rect.centery += int(self.landing_speed * dt)
            self.ship_rect.centerx += int((self.landing_x - self.ship_rect.centerx) / 10)
        else:
            self.ship_rect.centery = self.landing_y
            if self.delay_start_time is None:
                self.delay_start_time = pygame.time.get_ticks()


        # Calculate scaling based on distance
        if distance_to_landing >= 500:
            scaling_factor = 1 + self.scaling_rate * (800 - distance_to_landing)
        elif distance_to_landing < 500:
            scaling_factor = 1 - self.scaling_rate * (500 - distance_to_landing)
        else:
            scaling_factor = 1


        # Apply scaling to ship image
        self.ship_img = pygame.transform.scale(self.original_ship_img, (
            int(self.original_ship_img.get_width() * scaling_factor),
            int(self.original_ship_img.get_height() * scaling_factor)))
        self.ship_rect = self.ship_img.get_rect(center=(self.ship_rect.centerx, self.ship_rect.centery))

        if self.delay_start_time and pygame.time.get_ticks() - self.delay_start_time >= 1000:
            if not self.person_walking:
                self.person_visible = True
                self.person_walking = True

        if self.person_walking:
            self.person_frame_count += 1
            if self.person_frame_count >= 6:
                self.person_current_frame = (self.person_current_frame + 1) % len(self.person_frames)
                self.person_frame_count = 0
            self.person_position[0] += int(self.person_walking_speed * dt)

            if self.person_position[0] >= 925:
                self.person_visible = False
                self.person_walking = False

        # Update comets randomly
        if random.randrange(0, 1000) == 0:
            self.comets.append(Comet(self.screen.get_width(), self.screen.get_height()))
        self.comets = [comet for comet in self.comets if comet.x > -100]

    def render(self):
        self.screen.fill((0, 0, 0))

        # Draw stars
        for star in self.stars:
            star.draw(self.screen)

        # Draw comets
        for comet in self.comets:
            comet.draw(self.screen)

        # Draw planetoids
        for planetoid in self.planetoids:
            self.screen.blit(planetoid.image, planetoid.rect)

        # Draw spaceport
        self.screen.blit(self.spaceport_img, self.spaceport_rect)

        # Draw ship
        self.screen.blit(self.ship_img, self.ship_rect)

        # Draw walking person
        if self.person_visible:
            self.screen.blit(self.person_frames[self.person_current_frame], (self.person_position[0] + 40, self.landing_y - 13))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                self.run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_event_handler.handle_click(event.pos, event.button)
            elif event.type == pygame.KEYDOWN:
                # Add more key handling as necessary
                if event.key == pygame.K_SPACE:
                    print("Spacebar pressed!")  # Example action

    def run_scene(self):
        while self.run:
            dt = self.clock.tick(60) / 1000.0
            self.handle_events()
            self.update(dt)
            self.render()