import asyncio
import pygame
import pygame.sprite
import random

from button import Button, TransparentButton
from cockpit import Cockpit, Comms, Speedometer, Radar
from game_objects import SpaceWoman01
from game_state_manager import GameStateManager
from landing_scene import LandingScene
from mouse_event import MouseEventHandler
from ship import Ship
from stars import Star, Comet, Planetoid


async def main():
    # For displaying the debug text
    pygame.font.init()
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
    stick_back_img = Cockpit('images/starfighter02_stickback.png', screen)
    stick_forward_img = Cockpit('images/starfighter02_stickforward.png', screen)
    stick_left_img = Cockpit('images/starfighter02_stickleft.png', screen)
    stick_right_img = Cockpit('images/starfighter02_stickright.png', screen)
    speedometer = Speedometer((738, 724))
    radar_position = (513, 622)
    radar = Radar(radar_position, 80)

    NUM_STARS = 300
    stars = [Star(SCREEN_WIDTH, SCREEN_HEIGHT) for _ in range(NUM_STARS)]
    comets = []
    planetoids = pygame.sprite.LayeredUpdates()

    # intial scale = distance away
    planetoid_01 = Planetoid('images/green_planet01.png',
                             (600, 300),
                             "planetoid_01",
                             initial_scale=0.15,
                             scaling_rate=.00005,
                             orbit_speed=1,
                             max_scale=1)
    space_station_01 = Planetoid('images/space_station01.png',
                                 (-400, 400,),
                                 "space_station_01",
                                 initial_scale=.04,
                                 scaling_rate=.001,
                                 orbit_speed=2,
                                 max_scale=2)
    star_01 = Planetoid('images/star01.png',
                        (400, 400),
                        "star_01",
                        initial_scale=.2,
                        scaling_rate=0,
                        orbit_speed=.25)
    # Add sprites with a specific layer
    planetoids.add(star_01, layer=0)  # Ensure star_01 is on the bottom layer
    planetoids.add(planetoid_01, layer=1)
    planetoids.add(space_station_01, layer=2)

    def spacewoman_comms_routine():
        if not comms.is_fully_visible('spacewoman01'):
            comms.toggle_visibility()
        else:
            spacewoman01.dialogue_index += 1
        if spacewoman01.dialogue_index == len(spacewoman01.dialogue):
            comms.toggle_visibility()
            cockpit.instruments[11]['glow'] = False
            # direct to space station now
            game_state_manager.navpoint_001_active = True

    def landing_comms_routine():
        space_station_01 = next((p for p in planetoids if p.object_id == "space_station_01"), None)
        if space_station_01 and space_station_01.comms_distance and game_state_manager.navpoint_001_active:
            cockpit.instruments[12]['glow'] = True


    #onscreen nav point marker
    def draw_cross(surface, position, size=10, color=(255, 0, 0), thickness=2):
        x, y = position
        pygame.draw.line(surface, color, (x - size, y), (x + size, y), thickness)
        pygame.draw.line(surface, color, (x, y - size), (x, y + size), thickness)

    comms.add_portrait('spacewoman01',
                       'images/comms woman.png',
                       'images/comms woman 2.png',
                       (335, 150),
                       alpha=0)
    comms_in_button = TransparentButton(None,
                                     20,
                                     20,
                                     (830, 830),
                                     0,
                                     spacewoman_comms_routine,
                                     None,
                                     (255, 255, 255, 0),
                                     (255, 255, 255, 0),
                                     (255, 255, 255, 0))

    comms_out_button = TransparentButton(None,
                                         30,
                                         35,
                                         (775, 790),
                                         0,
                                         landing_comms_routine,
                                         None,
                                         (255, 255, 255, 0),
                                         (255, 255, 255, 0),
                                         (255, 255, 255, 0))

    pygame.mixer.music.load("./music/Lofi Beat 2.wav")
    pygame.mixer.music.set_volume(0.50)
    pygame.mixer.music.play(loops=-1)

    # Characters

    spacewoman01 = SpaceWoman01(dialogue=SpaceWoman01.dialogue,
                                position=(207, 209),
                                game_state_manager=game_state_manager,
                                comms_instance=comms)

    mouse_event_handler = MouseEventHandler(
        clickable_objects=[comms_in_button],
        interactive_objects=[spacewoman01],
        dropdown_menus=None)

    # avoid fat planets disappearing before fully off-screen
    planetoid_padding = 30

    # gamestate is not cutscene
    game_state_manager.in_gameplay = True

    run = True

    while run:
        if game_state_manager.in_gameplay:
            # Movement
            dt = clock.tick(60) / 1000.0
            keys = pygame.key.get_pressed()

            # temporary cutscene trigger
            if keys[pygame.K_SPACE]:  # change to condition for cutscene
                game_state_manager.switch_to_landing_scene()

            # Fast turn logic
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                yoke_pull = 5  # Increase the speed for debugging or fast movement
            else:
                yoke_pull = 1  # Reset to normal speed

            # For relative movement against starfield
            ship_yaw_change = ship.turn_speed * dt if keys[pygame.K_d] else -ship.turn_speed * dt if keys[
                pygame.K_a] else 0
            ship_pitch_change = ship.turn_speed * dt if keys[pygame.K_s] else -ship.turn_speed * dt \
                if keys[pygame.K_w] else 0

            # Update ship's orientation for star movement
            ship.angle += ship_yaw_change  # Assuming ship.angle incorporates both yaw and pitch

            # Relative location of space objects/illusion of movement
            for planetoid in planetoids:
                modified_orbit_speed = planetoid.orbit_speed * yoke_pull
                if keys[pygame.K_w]:
                    ship.pitch_down(dt)
                    if not planetoid.behind_player:
                        planetoid.position.y -= modified_orbit_speed
                        if planetoid.position.y <= 0 - planetoid_padding:
                            planetoid.behind_player = True
                            planetoid.is_visible = False
                    else:
                        planetoid.position.y += modified_orbit_speed
                        if planetoid.position.y >= SCREEN_HEIGHT + planetoid_padding:
                            planetoid.behind_player = False
                            planetoid.is_visible = True
                if keys[pygame.K_s]:
                    ship.pitch_down(-dt)
                    if not planetoid.behind_player:
                        planetoid.position.y += modified_orbit_speed
                        if planetoid.position.y >= SCREEN_HEIGHT + planetoid_padding:
                            planetoid.behind_player = True
                            planetoid.is_visible = False
                    else:
                        planetoid.position.y -= modified_orbit_speed
                        if planetoid.position.y <= 0 - planetoid_padding:
                            planetoid.behind_player = False
                            planetoid.is_visible = True
                if keys[pygame.K_a]:
                    ship.turn(-ship.turn_speed * dt)
                    if not planetoid.behind_player:
                        planetoid.position.x += modified_orbit_speed
                        if planetoid.position.x >= SCREEN_WIDTH + planetoid_padding:
                            planetoid.behind_player = True
                            planetoid.is_visible = False
                    else:
                        planetoid.position.x -= modified_orbit_speed
                        if planetoid.position.x <= 0 - planetoid_padding:
                            planetoid.behind_player = False
                            planetoid.is_visible = True
                if keys[pygame.K_d]:
                    ship.turn(ship.turn_speed * dt)
                    if not planetoid.behind_player:
                        planetoid.position.x -= modified_orbit_speed
                        if planetoid.position.x <= (0 - planetoid_padding):
                            planetoid.behind_player = True
                            planetoid.is_visible = False
                    else:
                        planetoid.position.x += modified_orbit_speed
                        if planetoid.position.x >= SCREEN_WIDTH + planetoid_padding:
                            planetoid.behind_player = False
                            planetoid.is_visible = True

                SCREEN_CENTER = pygame.Vector2(SCREEN_WIDTH / 2,
                                               SCREEN_HEIGHT / 2)  # screen center data for quadratic scaling MATHHHHASJKFHASKLJFASKJFBN
                planetoids.update(dt, ship_yaw_change, ship_pitch_change, ship.speed, SCREEN_CENTER)

            # Update stick image based on key press
            if keys[pygame.K_w]:
                current_stick_img = stick_forward_img
            elif keys[pygame.K_s]:
                current_stick_img = stick_back_img
            elif keys[pygame.K_a]:
                current_stick_img = stick_left_img
            elif keys[pygame.K_d]:
                current_stick_img = stick_right_img
            else:
                current_stick_img = cockpit

            # Throttle/ scaling speed
            if keys[pygame.K_UP]:  # Speed up
                ship.adjust_speed(10 * dt)
            if keys[pygame.K_DOWN]:  # Slow down
                ship.adjust_speed(-10 * dt)

            # event loop
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

            # Ships speed through stars
            ship_velocity_vector = ship.get_velocity_vector()
            for star in stars:
                star.update(ship_velocity_vector, dt)
                star.draw(screen)

            # An occasional comet
            if random.randrange(0, 1000) == 0:  # Adjust chances as needed
                comets.append(Comet(SCREEN_WIDTH, SCREEN_HEIGHT))
            comets = [comet for comet in comets if comet.x > -100]  # Adjust threshold as needed

            # Update and draw comets
            for comet in comets:
                comet.update(ship_yaw_change, ship_pitch_change, dt)
                comet.draw(screen)

            # Draw planetoid objects and navcross
            for planetoid in planetoids:
                if planetoid.is_visible:
                    screen.blit(planetoid.image, planetoid.rect)
                if planetoid.object_id == "space_station_01" and game_state_manager.navpoint_001_active:
                    # Calculate the center of the planetoid image to position the cross
                    center_x = planetoid.rect.centerx
                    center_y = planetoid.rect.centery
                    draw_cross(screen, (center_x, center_y))

            # Overlay the cockpit image after drawing the stars
            speedometer.update(ship.speed)
            speedometer.draw(screen)
            radar.draw(screen, planetoids, ship.position, game_state_manager.navpoint_001_active)
            current_stick_img.draw()

            comms_in_button.draw(screen)
            comms.update_portraits()  # updates fade effect
            comms.draw()

            comms_out_button.draw(screen)
            landing_comms_routine()

            # Comms dialogue draw
            if comms.is_fully_visible('spacewoman01'):
                spacewoman01.show_current_dialogue(screen, comms)

        elif game_state_manager.in_landing_scene:
            landing_scene = LandingScene(screen)
            landing_scene.run_scene()
            game_state_manager.switch_to_gameplay()

        pygame.display.flip()

        await asyncio.sleep(0)

        # Control the frame update rate for asyncio compatibility
        # Debug
        # velocity_text = f"Velocity: {ship.speed:.2f}"
        # velocity_surface = font.render(velocity_text, True, pygame.Color('white'))
        # screen.blit(velocity_surface, (20, 20))  # Position the text on the top-left corner
        # angle_text = f"Angle: {ship.angle}"
        # angle_surface = font.render(angle_text, True, pygame.Color('white'))
        # screen.blit(angle_surface, (20, 40))  # Position the text on the top-left corner
        # Switch to cutscene trigger

asyncio.run(main())
