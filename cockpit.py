import pygame
import random
import time

class Cockpit:
    def __init__(self, image_path, screen):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.screen = screen
        self.instruments = [
            # Red rect button left of yoke
            {'position': (442, 842), 'color': (255, 0, 0), 'size': (7, 5), 'shape': 'rectangle', 'glow': True,
             'fade_direction': 1, 'current_alpha': 128, 'max_brightness': 150, 'fade_speed': 3},
            # Yellow rect button left of yoke
            {'position': (465, 842), 'color': (210, 126, 56), 'size': (7, 5), 'shape': 'rectangle', 'glow': True,
             'fade_direction': 1, 'current_alpha': 128, 'max_brightness': 150, 'fade_speed': 3},
            # Panel left of radar, top left red
            {'position': (332, 550), 'color': (255, 99, 78), 'size': (10, 10), 'shape': 'circle', 'glow': True,
             'fade_direction': 1, 'current_alpha': 128, 'max_brightness': 200, 'fade_speed': 3},
            # Panel left of radar, top right red
            {'position': (373, 548), 'color': (255, 99, 78), 'size': (10, 10), 'shape': 'circle', 'glow': True,
             'fade_direction': 1, 'current_alpha': 128, 'max_brightness': 200, 'fade_speed': 5},
            # Panel left of radar, bottom right red
            {'position': (373, 596), 'color': (255, 99, 78), 'size': (10, 10), 'shape': 'circle', 'glow': True,
             'fade_direction': 1, 'current_alpha': 128, 'max_brightness': 200, 'fade_speed': 8},
            # Panel left of radar, top left yellow
            {'position': (330, 646), 'color': (255, 207, 116), 'size': (12, 12), 'shape': 'circle', 'glow': True,
             'fade_direction': 1, 'current_alpha': 128, 'max_brightness': 200, 'fade_speed': 1},
            # Panel left of radar, top right yellow
            {'position': (374, 647), 'color': (251, 219, 66), 'size': (12, 12), 'shape': 'circle', 'glow': True,
             'fade_direction': 1, 'current_alpha': 128, 'max_brightness': 150, 'fade_speed': 2},
            # Panel left of radar, bottom left yellow
            {'position': (332, 694), 'color': (251, 219, 66), 'size': (12, 12), 'shape': 'circle', 'glow': True,
             'fade_direction': 1, 'current_alpha': 128, 'max_brightness': 150, 'fade_speed': 2},
            # Panel left of radar, bottom right yellow
            {'position': (374, 694), 'color': (251, 219, 66), 'size': (12, 12), 'shape': 'circle', 'glow': True,
             'fade_direction': 1, 'current_alpha': 128, 'max_brightness': 150, 'fade_speed': 2},
            # Large round yellow dial far left, top
            {'position': (259, 618), 'color': (251, 219, 66), 'size': (15, 15), 'shape': 'circle', 'glow': True,
             'fade_direction': 1, 'current_alpha': 128, 'max_brightness': 150, 'fade_speed': 2},
            # Large round yellow dial far left, bottom
            {'position': (259, 686), 'color': (251, 219, 66), 'size': (15, 15), 'shape': 'circle', 'glow': True,
             'fade_direction': 1, 'current_alpha': 128, 'max_brightness': 150, 'fade_speed': 4},
            # Comms button
            {'position': (839, 840), 'color': (251, 125, 70), 'size': (10, 10), 'shape': 'circle', 'glow': True,
             'fade_direction': 1, 'current_alpha': 128, 'max_brightness': 150, 'fade_speed': 8},

        ]

    def draw(self):
        self.screen.blit(self.image, (0, 0))
        for instrument in self.instruments:
            if instrument['glow']:
                self.draw_glow(instrument['position'], instrument['color'], instrument['size'],
                               instrument['shape'], instrument)

    def draw_glow(self, position, color, size, shape='circle', instrument=None):
        if instrument:
            alpha = instrument['current_alpha']
            # Use fade_speed from the instrument's dictionary
            instrument['current_alpha'] += instrument['fade_direction'] * instrument['fade_speed']
            # Reverse fade direction if reaching the limits
            if instrument['current_alpha'] >= instrument['max_brightness'] or instrument['current_alpha'] <= 0:
                instrument['fade_direction'] *= -1
                # Ensure current_alpha stays within bounds
                instrument['current_alpha'] = max(0, min(instrument['current_alpha'], instrument['max_brightness']))
        else:
            alpha = 128  # Default alpha value

        glow_surface = pygame.Surface((size[0] * 2, size[1] * 2), pygame.SRCALPHA)
        glow_color = color + (alpha,)
        if shape == 'circle':
            pygame.draw.circle(glow_surface, glow_color, (size[0], size[1]), size[0])
        elif shape == 'rectangle':
            pygame.draw.rect(glow_surface, glow_color, (0, 0, size[0] * 2, size[1] * 2))
        position = (position[0] - size[0], position[1] - size[1])
        self.screen.blit(glow_surface, position)

class Comms:
    def __init__(self, screen):
        self.screen = screen
        self.portraits = []
        self.is_visible = False

    def add_portrait(self, ident, normal_image_path, static_image_path, position, alpha, static_duration=1, normal_duration=2, fade_speed=2):
        normal_image = pygame.image.load(normal_image_path).convert_alpha()
        static_image = pygame.image.load(static_image_path).convert_alpha()
        self.portraits.append({
            'id': ident,
            'normal_image': normal_image,
            'static_image': static_image,
            'position': position,
            'current_alpha': 0,
            'target_alpha': 0,
            'fade_speed': fade_speed,
            'use_static': False,
            'static_duration': static_duration,
            'normal_duration': normal_duration,
            'last_toggle_time': time.time(),
            'current_state_duration': normal_duration if not 'use_static' else static_duration
        })

    def set_portrait_alpha(self, index, alpha):
        # not currently implemented. maybe later
        if 0 <= index < len(self.portraits):
            self.portraits[index]['alpha'] = alpha


    def update_portraits(self):
        current_time = time.time()
        for portrait in self.portraits:
            # Update current_alpha towards target_alpha
            if portrait['current_alpha'] < portrait['target_alpha']:
                portrait['current_alpha'] += portrait['fade_speed']
                # Clamp value to not exceed target
                if portrait['current_alpha'] > portrait['target_alpha']:
                    portrait['current_alpha'] = portrait['target_alpha']
            elif portrait['current_alpha'] > portrait['target_alpha']:
                portrait['current_alpha'] -= portrait['fade_speed']
                # Clamp value to not fall below target
                if portrait['current_alpha'] < portrait['target_alpha']:
                    portrait['current_alpha'] = portrait['target_alpha']
            # Check for toggle based on state and duration
            elapsed_time = current_time - portrait['last_toggle_time']
            if (portrait['use_static'] and elapsed_time >= portrait['static_duration']) or \
                    (not portrait['use_static'] and elapsed_time >= portrait['normal_duration']):
                portrait['use_static'] = not portrait['use_static']
                portrait['last_toggle_time'] = current_time  # Update only for the toggled portrait
                portrait['normal_duration'] = random.randrange(1, 5)  # Optional reset **was 10/20
                portrait['static_duration'] = .1

    def toggle_visibility(self):
        current_time = time.time()
        self.is_visible = not self.is_visible
        # Update target alpha and potentially reset durations (depending on desired behavior)
        target_alpha = 85 if self.is_visible else 0
        for portrait in self.portraits:
            if self.is_visible and portrait['current_alpha'] == 85 and target_alpha == 85:
                portrait['current_alpha'] = 0  # Ensure fade in from 0
            portrait['target_alpha'] = target_alpha
            portrait['last_toggle_time'] = current_time

    def draw(self):
        # Draw portraits regardless of is_visible, but use current_alpha to control visibility
        for portrait in self.portraits:
            image = portrait['static_image'] if portrait['use_static'] else portrait['normal_image']
            temp_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)
            temp_surface.blit(image, (0, 0))
            temp_surface.set_alpha(portrait['current_alpha'])
            self.screen.blit(temp_surface, portrait['position'])

    def is_fully_visible(self, portrait_id):
        for portrait in self.portraits:
            return all(portrait['current_alpha'] == 85 for portrait in self.portraits)

class Speedometer:
    def __init__(self, position, font_size=18, font_color=(255, 255, 255), box_color=(0, 0, 0), box_padding=10,
                 threshold=0.01, border_radius=10):
        pygame.font.init()
        self.font = pygame.font.SysFont('lucidasanstypewriter', font_size)
        self.font_color = font_color
        self.box_color = box_color
        self.position = position  # This position now represents the top-left corner of the black box
        self.box_padding = box_padding
        self.threshold = threshold
        self.border_radius = border_radius  # New attribute for rounded corners
        self.last_speed = None
        self.current_speed_surface = None
        # Initially, we don't know the size of the box, so set it to 0
        self.box_width = 0
        self.box_height = 0

    def update(self, speed):
        if self.last_speed is None or abs(speed - self.last_speed) > self.threshold:
            speed_text = f"VELOCITY: {speed:.2f}"
            self.current_speed_surface = self.font.render(speed_text, True, self.font_color)
            self.last_speed = speed
            # Update the box size based on the new text dimensions plus padding
            self.box_width = 160
            self.box_height = 50

    def draw(self, surface):
        if self.current_speed_surface:
            # Calculate the center position for the text within the box
            text_x = self.position[0] + (self.box_width - self.current_speed_surface.get_width()) // 2
            text_y = self.position[1] + (self.box_height - self.current_speed_surface.get_height()) // 2

            # Draw the black box with rounded corners
            box_rect = pygame.Rect(self.position[0], self.position[1], self.box_width, self.box_height)
            pygame.draw.rect(surface, self.box_color, box_rect, border_radius=self.border_radius)

            # Then draw the speed text over it
            surface.blit(self.current_speed_surface, (text_x, text_y))

class Radar:
    def __init__(self, center_position, radius, radar_color=(0, 255, 0), background_color=(20, 20, 20), border_color=(255, 255, 255), border_thickness=2, blink_duration=0.5):
        pygame.font.init()
        self.center_position = center_position
        self.radius = radius
        self.radar_color = radar_color
        self.background_color = background_color
        self.border_color = border_color
        self.border_thickness = border_thickness
        self.blink_duration = blink_duration
        self.last_blink_time = time.time()
        self.blink_state = True

    def draw(self, surface, planetoids, ship_position):
        current_time = time.time()
        if current_time - self.last_blink_time > self.blink_duration:
            self.blink_state = not self.blink_state
            self.last_blink_time = current_time

        pygame.draw.circle(surface, self.background_color, self.center_position, self.radius)
        pygame.draw.circle(surface, self.border_color, self.center_position, self.radius, self.border_thickness)

        for planetoid in planetoids:
            self._draw_planetoid_on_radar(surface, planetoid, ship_position)

    def _draw_planetoid_on_radar(self, surface, planetoid, ship_position):
        # Calculate the relative position of the planetoid to the ship
        rel_x = planetoid.position.x - ship_position.x
        rel_y = planetoid.position.y - ship_position.y

        # Scale these positions to fit on the radar
        scale_factor = self.radius / (pygame.display.get_surface().get_width() / 2)
        radar_x = int(self.center_position[0] + rel_x * scale_factor)
        radar_y = int(self.center_position[1] + rel_y * scale_factor)

        # Draw the planetoid on the radar
        if abs(rel_x) <= self.radius / scale_factor and abs(rel_y) <= self.radius / scale_factor:
            if planetoid.behind_player:
                if self.blink_state:
                    pygame.draw.circle(surface, self.radar_color, (radar_x, radar_y), 2)
            else:
                pygame.draw.circle(surface, self.radar_color, (radar_x, radar_y), 2)
