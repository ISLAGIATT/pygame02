import pygame
class Button:
    def __init__(self, color, x, y, width, height, text='', alpha=255):
        self.color = color
        self.alpha = alpha
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen, outline=None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        # Create a surface with the specified alpha transparency
        button_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, (self.color[0], self.color[1], self.color[2], self.alpha),
                         (0, 0, self.width, self.height), 0)
        screen.blit(button_surface, (self.x, self.y))

        if self.text != '':
            font = pygame.font.Font(None, 24)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def set_alpha(self, alpha):
        self.alpha = alpha

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False

class TransparentButton:
    def __init__(self, text, width, height, pos, elevation, action, image, color, shadow, hover):
        self.action = action
        self.width = width
        self.height = height
        self.x = pos[0]
        self.y = pos[1]
        self.text = text
        self.elevation = elevation
        self.original_y_pos = pos[1]
        self.color = color
        self.color_shadow = shadow
        self.hover = hover
        self.clicked = False
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = color
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = shadow
        font = pygame.font.SysFont('rockwell', 50)
        self.text_surf = font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def is_over(self, pos):
        top_rect = self.top_rect.copy()
        top_rect.inflate_ip(self.elevation, self.elevation)
        return top_rect.collidepoint(pos)

    def draw(self, screen):
        action = False
        pos = pygame.mouse.get_pos()
        top_rect = self.top_rect.copy()
        bottom_rect = self.bottom_rect.copy()
        bottom_rect.x += 20
        bottom_rect.y += 20
        if top_rect.collidepoint(pos):
            self.top_color = self.color
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
                bottom_rect.inflate_ip(self.elevation, self.elevation)
                top_rect.inflate_ip(self.elevation, self.elevation)

            elif pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False
                action = True
            self.top_color = self.hover
        else:
            self.top_color = self.color

        bottom_surf = pygame.Surface(bottom_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(bottom_surf, self.bottom_color, (0, 0, *bottom_rect.size), border_radius=12)
        screen.blit(bottom_surf, bottom_rect.topleft)

        top_surf = pygame.Surface(top_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(top_surf, self.top_color, (0, 0, *top_rect.size), border_radius=12)
        screen.blit(top_surf, top_rect.topleft)

        screen.blit(self.text_surf, self.text_rect)
        return action

    def handle_click(self, mouse_pos, button=1):
        # Call the action (function) passed to this button if it's provided
        if self.action and self.is_over(mouse_pos):
            self.action()
