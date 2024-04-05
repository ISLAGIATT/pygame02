import asyncio
import pygame
import pygame.sprite
import random

from button import Button, TransparentButton
from cockpit import Cockpit, Comms, Speedometer, Radar
from game_objects import SpaceWoman01
from game_state_manager import GameStateManager
from mouse_event import MouseEventHandler
from ship import Ship
from stars import Star, Comet, Planetoid


async def main():
    # For displaying the debug text, initialize a Pygame font
    pygame.font.init()  # Initialize font module
    font = pygame.font.SysFont('Arial', 24)

    # Define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    GREY = (32, 32, 32)

    pygame.init()

    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 1024
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    game_state_manager = GameStateManager()
    comms = Comms(screen)
    clock = pygame.time.Clock()

    ship = Ship(position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), speed=.5, turn_speed=800)
    cockpit = Cockpit('images/starfighter01.png', screen)
    speedometer = Speedometer((738, 724))
    radar_position = (513, 622)
    radar = Radar(radar_position, 80)

    NUM_STARS = 300
    stars = [Star(SCREEN_WIDTH, SCREEN_HEIGHT) for _ in range(NUM_STARS)]
    comets = []
    planetoids = pygame.sprite.Group()

    # intial scale = distance away

    planetoid_01 = Planetoid('images/green_planet01.png',
                             (600, 300),
                             initial_scale=0.15,
                             scaling_rate=.0005)
    space_station_01 = Planetoid('images/space_station01.png',
                                 (-400, 400,),
                                 initial_scale=.04,
                                 scaling_rate=.005)
    star_01 = Planetoid('images/star01.png', (400,400),
                        # ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)),
                        initial_scale=.2,
                        scaling_rate=0) # static background
    planetoids.add(planetoid_01, space_station_01, star_01)


    def comms_routine():
        if not comms.is_fully_visible('spacewoman01'):
            comms.toggle_visibility()
        else:
            spacewoman01.dialogue_index += 1
        if spacewoman01.dialogue_index == len(spacewoman01.dialogue):
            comms.toggle_visibility()
            cockpit.instruments[11]['glow'] = False

    comms.add_portrait('spacewoman01',
                       'images/comms woman.png',
                       'images/comms woman 2.png',
                       (335, 150),
                       alpha=0)
    comms_button = TransparentButton(None,
                                     20,
                                     20,
                                     (830, 830),
                                     0,
                                     comms_routine,
                                     None,
                                     (255, 255, 255, 0),
                                     (255, 255, 255, 0),
                                     (255, 255, 255, 0))

    pygame.mixer.music.load("./music/Lofi Beat 2.wav")
    pygame.mixer.music.set_volume(0.50)
    pygame.mixer.music.play(loops=-1)

    # Characters

    spacewoman01 = SpaceWoman01(dialogue=SpaceWoman01.dialogue,
                                position=(207,209),
                                game_state_manager=game_state_manager,
                                comms_instance=comms)

    mouse_event_handler = MouseEventHandler(
        clickable_objects=[comms_button],
        interactive_objects=[spacewoman01],
        dropdown_menus=None)

    # orbit speed = perspective turn speed
    planetoid_orbit_speed = 1
    # avoid fat planets disappearing before fully off-screen
    planetoid_padding = 30
    run = True
    while run:
        # Movement
        dt = clock.tick(60) / 1000.0  # Converts milliseconds to seconds
        keys = pygame.key.get_pressed()

        # For relative movement against starfield
        ship_yaw_change = ship.turn_speed * dt if keys[pygame.K_d] else -ship.turn_speed * dt if keys[pygame.K_a] else 0
        ship_pitch_change = ship.turn_speed * dt if keys[pygame.K_s] else -ship.turn_speed * dt if keys[
            pygame.K_w] else 0

        # Update ship's orientation
        ship.angle += ship_yaw_change  # Assuming ship.angle incorporates both yaw and pitch

        # Relative location of space objects
        for planetoid in planetoids:
            if keys[pygame.K_w]:
                ship.pitch_down(dt)
                if not planetoid.behind_player:
                    planetoid.position.y -= planetoid_orbit_speed
                    if planetoid.position.y <= 0 - planetoid_padding:
                        planetoid.behind_player = True
                        planetoid.is_visible = False
                else:
                    planetoid.position.y += planetoid_orbit_speed
                    if planetoid.position.y >= SCREEN_HEIGHT + planetoid_padding:
                        planetoid.behind_player = False
                        planetoid.is_visible = True
            if keys[pygame.K_s]:
                ship.pitch_down(-dt)
                if not planetoid.behind_player:
                    planetoid.position.y += planetoid_orbit_speed
                    if planetoid.position.y >= SCREEN_HEIGHT + planetoid_padding:
                        planetoid.behind_player = True
                        planetoid.is_visible = False
                else:
                    planetoid.position.y -= planetoid_orbit_speed
                    if planetoid.position.y <= 0 - planetoid_padding:
                        planetoid.behind_player = False
                        planetoid.is_visible = True
            if keys[pygame.K_a]:
                ship.turn(-ship.turn_speed * dt)
                if not planetoid.behind_player:
                    planetoid.position.x += planetoid_orbit_speed
                    if planetoid.position.x >= SCREEN_WIDTH + planetoid_padding:
                        planetoid.behind_player = True
                        planetoid.is_visible = False
                else:
                    planetoid.position.x -= planetoid_orbit_speed
                    if planetoid.position.x <= 0 - planetoid_padding:
                        planetoid.behind_player = False
                        planetoid.is_visible = True
            if keys[pygame.K_d]:
                ship.turn(ship.turn_speed * dt)
                if not planetoid.behind_player:
                    planetoid.position.x -= planetoid_orbit_speed
                    if planetoid.position.x <= (0 - planetoid_padding):
                        planetoid.behind_player = True
                        planetoid.is_visible = False
                else:
                    planetoid.position.x += planetoid_orbit_speed
                    if planetoid.position.x >= SCREEN_WIDTH + planetoid_padding:
                        planetoid.behind_player = False
                        planetoid.is_visible = True

            planetoids.update(dt, ship_yaw_change, ship_pitch_change, ship.speed)

        # Throttle/ scaling speed
        if keys[pygame.K_UP]:  # Speed up
            ship.adjust_speed(10 * dt)
        if keys[pygame.K_DOWN]:  # Slow down
            ship.adjust_speed(-10 * dt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                button = event.button
                print(f"Mouse pos: {mouse_pos}")
                mouse_event_handler.handle_click(event.pos, event.button)

        # Fill the screen with black to clear old frames
        screen.fill(BLACK)
        ship_velocity_vector = ship.get_velocity_vector()


        for star in stars:
            star.update(ship_velocity_vector, dt)
            star.draw(screen)

        # An occasional comet
        if random.randrange(0, 1000) == 0:  # Adjust chances as needed
            comets.append(Comet(SCREEN_WIDTH, SCREEN_HEIGHT))
        comets = [comet for comet in comets if comet.x > -100]  # Adjust threshold as needed
        # # Update and draw comets
        for comet in comets:
            comet.update(ship_yaw_change, ship_pitch_change, dt)
            comet.draw(screen)

        for planetoid in planetoids:
            if planetoid.is_visible:
                screen.blit(planetoid.image, planetoid.rect)

        # Overlay the cockpit image after drawing the stars
        speedometer.update(ship.speed)
        speedometer.draw(screen)
        radar.draw(screen, planetoids, ship.position)
        cockpit.draw()
        comms_button.draw(screen)
        comms.update_portraits()  # updates fade effect
        comms.draw()


        # Comms dialogue draw
        if comms.is_fully_visible('spacewoman01'):
            spacewoman01.show_current_dialogue(screen, comms)


        # Debug
        # velocity_text = f"Velocity: {ship.speed:.2f}"
        # velocity_surface = font.render(velocity_text, True, pygame.Color('white'))
        # screen.blit(velocity_surface, (20, 20))  # Position the text on the top-left corner
        # angle_text = f"Angle: {ship.angle}"
        # angle_surface = font.render(angle_text, True, pygame.Color('white'))
        # screen.blit(angle_surface, (20, 40))  # Position the text on the top-left corner

        pygame.display.flip()

        await asyncio.sleep(0)  # Control the frame update rate for asyncio compatibility

asyncio.run(main())