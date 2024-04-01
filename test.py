

import pygame

pygame.init()

# Screen setup
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Object setup
object_color = (255, 0, 0)
object_size = 20
object_x = screen_width // 2
object_y = screen_height // 2
object_behind_player = False  # To track if the object is "behind" the player


def update_object_surface(opaque=True):
    """Updates the object's surface based on its visibility state."""
    global object_surface
    alpha = 255 if opaque else 128  # Full opacity or semi-transparent
    object_surface = pygame.Surface((2 * object_size, 2 * object_size), pygame.SRCALPHA)
    temp_color = object_color + (alpha,)  # Add alpha to the object's color
    pygame.draw.circle(object_surface, temp_color, (object_size, object_size), object_size)


update_object_surface()  # Initialize the surface with the object being opaque

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if not object_behind_player:
                    object_x -= 50  # Move left
                    if object_x <= 0:
                        object_behind_player = True  # Indicate that the object is now "behind" the player
                        update_object_surface(opaque=False)  # Make the object semi-transparent
                        object_x = 0
                else:
                    object_x += 50
                    if object_x >= screen_width:
                        object_behind_player = False  # Object is no longer "behind" the player
                        update_object_surface(opaque=True)  # Make the object opaque again
            elif event.key == pygame.K_LEFT:
                if not object_behind_player:
                    object_x += 50  # Move left
                    if object_x >= screen_width:
                        object_behind_player = True  # Indicate that the object is now "behind" the player
                        update_object_surface(opaque=False)  # Make the object semi-transparent
                else:
                    object_x -= 50
                    if object_x <= 0:
                        object_behind_player = False  # Object is no longer "behind" the player
                        update_object_surface(opaque=True)  # Make the object opaque again
            elif event.key == pygame.K_UP:
                if not object_behind_player:
                    object_y += 50  # Move down
                    if object_y >= screen_height:
                        object_behind_player = True  # Indicate that the object is now "behind" the player
                        update_object_surface(opaque=False)  # Make the object semi-transparent
                else:
                    object_y -= 50
                    if object_y <= 0:
                        object_behind_player = False  # Object is no longer "behind" the player
                        update_object_surface(opaque=True)  # Make the object opaque again
            elif event.key == pygame.K_DOWN:
                if not object_behind_player:
                    object_y -= 50  # Move down
                    if object_y <= 0:
                        object_behind_player = True  # Indicate that the object is now "behind" the player
                        update_object_surface(opaque=False)  # Make the object semi-transparent
                else:
                    object_y += 50
                    if object_y >= screen_height:
                        object_behind_player = False  # Object is no longer "behind" the player
                        update_object_surface(opaque=True)  # Make the object opaque again



    screen.fill((0, 0, 0))
    screen.blit(object_surface, (object_x - object_size, object_y - object_size))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

#TODO add logic for an invisible planet offsides to be able to turn visible when back within FOV