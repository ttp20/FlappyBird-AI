import pygame
import os

# path to bird images
bird1 = pygame.image.load(os.path.join("imgs", "bird1.png"))
bird2 = pygame.image.load(os.path.join("imgs", "bird2.png"))
bird3 = pygame.image.load(os.path.join("imgs", "bird1.png"))

pygame.font.init()

class Settings:

    # class variables
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 800
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # generation
    GEN = 0

    # imgs
    BIRD_IMGS = [pygame.transform.scale2x(bird1), pygame.transform.scale2x(bird2), pygame.transform.scale2x(bird3)]
    PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
    GROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
    BACKGROUNG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

    # font
    FONT = pygame.font.SysFont('comicsans', 30)

    def __init__(self):
        pass
