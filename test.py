import pygame

from landing_scene import LandingScene

pygame.mixer.init()
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 1024
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

landing_scene = LandingScene(screen)

landing_scene.run_scene()