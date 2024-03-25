import pygame

class Dialogue:
    def __init__(self):
        SCREEN_WIDTH = 1024
        SCREEN_HEIGHT = 1024
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.BLACK = (0, 0, 0)

    def draw_wrapped_text(self, text, max_characters_per_line, font, color, pos):
        words = text.split()
        lines = []
        current_line = ''
        for word in words:
            if font.size(current_line + word)[0] <= max_characters_per_line * font.size('A')[0]:
                current_line += ' ' + word
            else:
                lines.append(current_line.lstrip())
                current_line = word
        lines.append(current_line.lstrip())

        # Calculate the size of the dialogue bubble
        max_width = max(font.size(line)[0] for line in lines)
        total_height = sum(font.size(line)[1] for line in lines)
        bubble_rect = pygame.Rect(pos[0] - 10, pos[1] - 10, max_width + 20, total_height + 20)
        pygame.draw.rect(self.screen, self.BLACK, bubble_rect, border_radius=10)  # Draw the rounded rectangle

        y = pos[1]
        for line in lines:
            text_surface = font.render(line, True, color)
            self.screen.blit(text_surface, (pos[0], y))
            y += font.size(line)[1]  # Move to the next line
        return bubble_rect

    def draw_dialogue(self, text, color, pos):
        # Early return if text is empty or None
        if not text:
            return None  # Or an appropriate action

        font = pygame.font.Font(None, 36)
        max_characters_per_line = 25
        # Proceed with drawing the text, assuming it's valid
        dialogue_rect = self.draw_wrapped_text(text, max_characters_per_line, font, color, pos)
        return dialogue_rect
