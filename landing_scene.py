import asyncio
import pygame
import pygame.sprite
import random

from stars import Star, Comet, Planetoid
from mouse_event import MouseEventHandler

pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 1024
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
mouse_event_handler = MouseEventHandler

spaceport_img = pygame.image.load('images/space_station_landing01.png')
spaceport_rect = spaceport_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

original_ship_img = pygame.image.load('images/ship_landing.png')
ship_rect = original_ship_img.get_rect(
    center=(SCREEN_WIDTH // 2, -original_ship_img.get_height()))  # Start above the screen
landing_x = 559
landing_y = 906

person_sprite_sheet_image = pygame.image.load('images/PlayerWalk 48x48.png').convert_alpha()

def get_person_image(x, y, width, height):
    image = pygame.Surface((width, height), pygame.SRCALPHA)
    image.blit(person_sprite_sheet_image, (0, 0), (x, y, width, height))
    return image


person_frame_width = 48  # Assuming each frame is 48x48
person_frame_height = 48
person_frames = []
num_person_frames = 8  # Total frames in the sprite sheet

for i in range(num_person_frames):
    frame = get_person_image(i * person_frame_width, 0, person_frame_width, person_frame_height)
    person_frames.append(frame)

person_current_frame = 0
person_frame_count = 0
person_position = [ship_rect.centerx, ship_rect.bottom]  # Starting position
person_walking_speed = 150  # Pixels per second
person_walking = False
person_visible = False


NUM_STARS = 300
stars = [Star(SCREEN_WIDTH, SCREEN_HEIGHT) for _ in range(NUM_STARS)]
comets = []
planetoids = pygame.sprite.LayeredUpdates()

planetoid_01 = Planetoid('images/green_planet01.png',
                         (600, 300),
                         "planetoid_01",
                         initial_scale=0.15,
                         scaling_rate=.00005,
                         orbit_speed=1)

star_01 = Planetoid('images/star01.png',
                    (400, 400),
                    "star_01",
                    initial_scale=.2,
                    scaling_rate=0,
                    orbit_speed=.25)
# Add sprites with a specific layer
planetoids.add(star_01, layer=0)  # Ensure star_01 is on the bottom layer
planetoids.add(planetoid_01, layer=1)

pygame.mixer.music.load("./music/Ancient-Game-Menu.mp3")
pygame.mixer.music.set_volume(0.50)
pygame.mixer.music.play(loops=-1)

run = True
landing_speed = 175  # Pixels per second
scaling_rate = 0.001  # Adjust this rate as needed

while run:
    dt = clock.tick(60) / 1000.0  # Converts milliseconds to seconds
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            button = event.button
            print(f"Mouse pos: {mouse_pos}")
            mouse_event_handler.handle_click(event.pos, event.button)

    screen.fill((0, 0, 0))

    for star in stars:
        star.draw(screen)
    # An occasional comet
    if random.randrange(0, 1000) == 0:  # Adjust chances as needed
        comets.append(Comet(SCREEN_WIDTH, SCREEN_HEIGHT))
    comets = [comet for comet in comets if comet.x > -100]  # Adjust threshold as needed

    # # Update and draw comets
    for comet in comets:
        comet.draw(screen)

    for planetoid in planetoids:
        screen.blit(planetoid.image, planetoid.rect)

    # Draw the spaceport
    screen.blit(spaceport_img, spaceport_rect)

    # Calculate the distance to the landing zone and adjust landing speed and scaling
    distance_to_landing = landing_y - ship_rect.centery

    if 800 > distance_to_landing >= 500:
        # Scale larger as the ship approaches 800px to 500px away
        scaling_factor = 1 + scaling_rate * (800 - distance_to_landing)
    elif distance_to_landing < 500:
        # Scale smaller as the ship gets closer than 500px
        scaling_factor = 1 - scaling_rate * (500 - distance_to_landing)
    else:
        scaling_factor = 1

    ship_img = pygame.transform.scale(original_ship_img, (
        int(original_ship_img.get_width() * scaling_factor), int(original_ship_img.get_height() * scaling_factor)))
    ship_rect = ship_img.get_rect(center=(SCREEN_WIDTH // 2, ship_rect.centery))

    if distance_to_landing < 200:
        landing_speed = 100  # Reduce speed by 75%

    if ship_rect.centery < landing_y:
        ship_rect.centery += int(landing_speed * dt)
        ship_rect.centerx += int((landing_x - ship_rect.centerx) / 10)  # Gradually move x-position
    else:
        ship_rect.centery = landing_y  # Ensure the ship doesn't go below the landing point
        if abs(ship_rect.centerx - landing_x) < 5:
            ship_rect.centerx = landing_x

    if ship_rect.centery == landing_y and not person_walking:
        person_visible = True
        person_walking = True  # Start walking animation once the ship has landed
        print("Walking animation started.")  # Debug print

    if person_walking:
        person_frame_count += 1
        if person_frame_count >= 6:
            person_current_frame = (person_current_frame + 1) % num_person_frames
            person_frame_count = 0
        person_position[0] += int(person_walking_speed * dt)  # Move right

        if person_position[0] >= 950:
            person_visible = False
            person_walking = False

        if person_visible:
            screen.blit(person_frames[person_current_frame], (person_position[0], landing_y - person_frame_height))

        # Debug prints
        print(f"Animating: {person_position[0]}, Frame: {person_current_frame}")

        # Stop walking when reaching the right edge of the screen
        if person_position[0] > SCREEN_WIDTH:
            person_walking = False

    screen.blit(ship_img, ship_rect)

    pygame.display.flip()
