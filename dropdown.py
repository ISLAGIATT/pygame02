import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (170, 170, 170)

class DropdownMenu:
    def __init__(self, x, y, option_list, action_map, game_state_manager, w=100, h=30, color=(255, 255, 255),
                 highlight_color=(200, 200, 200), font=None, button=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.highlight_color = highlight_color
        self.option_list = option_list
        self.action_map = action_map
        self.game_state_manager = game_state_manager
        self.is_visible = False
        self.button = button
        if font is None:
            self.font = pygame.font.SysFont(None, 24)
        else:
            self.font = font

    def draw(self, surf):
        if not self.is_visible:
            return

        mouse_pos = pygame.mouse.get_pos()
        for i, text in enumerate(self.option_list):
            # Correctly calculate the position and size for each option's rectangle
            option_rect = pygame.Rect(self.x, self.y + i * self.h, self.w, self.h)

            # Determine the color based on mouse hover
            if option_rect.collidepoint(mouse_pos):
                color = self.highlight_color
            else:
                color = self.color

            # Draw the rectangle for the option
            pygame.draw.rect(surf, color, option_rect)

            # Render the text for the option
            msg = self.font.render(text, True, BLACK)
            msg_rect = msg.get_rect(center=option_rect.center)
            surf.blit(msg, msg_rect)

    def is_over_option(self, pos):
        for i, option in enumerate(self.option_list):
            # Calculate the rectangle for each option dynamically
            option_rect = pygame.Rect(self.x, self.y + i * self.h, self.w, self.h)
            if option_rect.collidepoint(pos):
                return i  # Return the index of the option that is being hovered over
        return None  # Return None if no option is hovered over

    def execute_action(self, option):
        if option in self.action_map:
            self.action_map[option]()

    def toggle_visibility(self):
        if not self.is_visible:
            # Close any other open dropdowns before showing this one
            self.game_state_manager.open_dropdown(self)
        else:
            # Directly call the method to hide this dropdown
            self.game_state_manager.close_dropdown(self)

    def close(self):
        # Method to programmatically close this dropdown
        self.is_visible = False