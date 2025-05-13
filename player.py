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
    def draw(self, window: pygame.Surface, scale: int):
        player = drawRect(window, (self.x*scale, self.y*scale), (40*scale, 100*scale), color = (255,255,255))
        self.rect = player.rect