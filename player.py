# Get libraries
from rectangles import drawRect
import pygame
pygame.init()
class Player:
    def __init__(self):
        # Easier for legibility
        self.x = 200
        self.y = 0
        self.grav = 0
        self.center = 200
        self.grounded = False
        self.jumpcount = 0
        self.jumplimit = 0
        self.level = 1
        self.image = pygame.image.load('images\\char.jpg').convert_alpha()
    def draw(self, window: pygame.Surface, scale: float):
        player = drawRect(window, (self.x, self.y), (40, 100), texture = self.image, scale = scale)
        self.rect = player.rect