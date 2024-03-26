import pygame.time
from dialogue import Dialogue
from cockpit import Comms


class InteractiveObject:
    MUSTARD = (199, 142, 0)
    RED = (199, 0, 57)
    TANGERINE = (255, 87, 51)
    MAGENTA = (204, 0, 204)
    PALE_GREEN = (218, 247, 166)
    AQUAMARINE = (0, 255, 255)

    def __init__(self, dialogue, position, game_state_manager, size=(100, 30)):
        self.dialogue = dialogue
        self.position = position
        self.size = size
        self.is_visible = False
        self.dialogue_index = 0
        self.dialogue_instance = Dialogue()
        self.game_state_manager = game_state_manager

    def toggle_visibility(self):
        self.is_visible = not self.is_visible

    def advance_dialogue(self):
        self.dialogue_index += 1
        if self.dialogue_index >= len(self.dialogue):
            self.dialogue_index = 0


class SpaceWoman01(InteractiveObject):
    dialogue = ["attention, to all available pilots",
                "be advised there is a developing situation on Galeb, near the system's asteroid belt",
                "proceed with caution and report to mainstation as soon as possible",
                "terran activity has been logged in the area recently"]

    def __init__(self, dialogue, position, game_state_manager, comms_instance):
        super().__init__(dialogue, game_state_manager, position)
        self.last_show_time = 0
        self.comms_instance = comms_instance


    def handle_click(self, mouse_pos, button):
        if button == 1:
            self.dialogue = self.dialogue

        self.last_show_time = pygame.time.get_ticks()

    def show_current_dialogue(self, screen, comms):
        # if self.dialogue:
        #     if pygame.time.get_ticks() - self.last_show_time > 3500:
        #         self.is_visible = False
        #         self.last_show_time = 0
        #     else:
        if self.dialogue:
            if 0 <= self.dialogue_index < len(self.dialogue):
                current_text = self.dialogue[self.dialogue_index]
                self.current_dialogue_rect = self.dialogue_instance.draw_dialogue(
                    text=current_text, color=self.MAGENTA, pos=(318, 72))
