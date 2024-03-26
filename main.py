import asyncio
import pygame
import random
import time

from button import Button, TransparentButton
from cockpit import Cockpit, Comms
from dialogue import Dialogue
from game_objects import SpaceWoman01
from game_state_manager import GameStateManager
from mouse_event import MouseEventHandler
from stars import Star, Comet


async def main():
    # Define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    GREY = (32, 32, 32)

    pygame.init()
    game_state_manager = GameStateManager()
    clock = pygame.time.Clock()

    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 1024
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    cockpit = Cockpit('images/starfighter01.png', screen)
    NUM_STARS = 200
    stars = [Star(SCREEN_WIDTH, SCREEN_HEIGHT) for _ in range(NUM_STARS)]
    comets = []

    comms = Comms(screen)

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

    run = True

    while run:
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

        # An occasional comet
        if random.randrange(0, 1000) == 0:  # Adjust chances as needed
            comets.append(Comet(SCREEN_WIDTH, SCREEN_HEIGHT))
        comets = [comet for comet in comets if comet.x > -100]  # Adjust threshold as needed
        # Update and draw comets
        for comet in comets:
            comet.update()
            comet.draw(screen)

        # Update star positions
        for star in stars:
            star.update()

        # Draw each star
        for star in stars:
            star.draw(screen)

        # Overlay the cockpit image after drawing the stars
        cockpit.draw()
        comms_button.draw(screen)
        comms.update_portraits()  # updates fade effect
        comms.draw()
        if comms.is_fully_visible('spacewoman01'):
            spacewoman01.show_current_dialogue(screen, comms)

        pygame.display.update()

        await asyncio.sleep(0)  # Control the frame update rate for asyncio compatibility

        # Control the frame rate for smooth animations
        clock.tick(60)  # Limit to 60 frames per second


asyncio.run(main())
