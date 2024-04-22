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
        if self.dialogue:
            if 0 <= self.dialogue_index < len(self.dialogue):
                current_text = self.dialogue[self.dialogue_index]
                self.current_dialogue_rect = self.dialogue_instance.draw_dialogue(
                    text=current_text, color=self.MAGENTA, pos=(318, 72))


class StationChief01(InteractiveObject):
    dialogue = [
        ("StationChief", "SHUTTLECRAFT. STATE YOUR BUSINESS."),
        ("POV", "callsign kneecap 421 coming home"),
        ("StationChief", "UNDERSTOOD. PLEASE FIND YOUR WAY TO DOCK 119"),
        ("StationChief", "THERE IS A MESSAGE WAITING FOR YOU AT THE BROKEN DOMINO"),
        ("POV", "thanks chuck"),
        ("StationChief", "YES")
    ]

    def __init__(self, dialogue, position, game_state_manager, comms_instance, cockpit_instance):
        super().__init__(dialogue, game_state_manager, position)
        self.game_state_manager = game_state_manager
        self.last_show_time = 0
        self.dialogue_index = 0
        self.comms_instance = comms_instance
        self.cockpit_instance = cockpit_instance

    def handle_click(self, mouse_pos, button):
        if button == 1 and self.cockpit_instance.instruments[12]['glow']:
            if not self.comms_instance.is_fully_visible('stationchief01'):
                self.comms_instance.toggle_visibility('stationchief01')
            else:
                self.dialogue_index += 1
            if self.dialogue_index == len(self.dialogue):
                self.comms_instance.toggle_visibility('stationchief01')
                self.game_state_manager.good_to_land = True

    def show_current_dialogue(self, screen):
        font = pygame.font.SysFont('Arial', 24)
        if self.dialogue and 0 <= self.dialogue_index < len(self.dialogue):
            speaker, current_text = self.dialogue[self.dialogue_index]

            if speaker == "StationChief":
                color = (255, 0, 0)  # Red for Station Chief
                position = (318, 72)
            else:
                color = (0, 255, 0)  # Green for POV
                position = (377, 676)

            self.dialogue_instance.draw_dialogue(current_text, color, position)
