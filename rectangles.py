# Library Import
import pygame
pygame.init()
# Get Rectangle
class drawRect:
    def __init__(self, window, pos: tuple, size: tuple, **kwargs):
        # Get color or texture if it exists
        color = kwargs.get('color',None)
        texture = kwargs.get("texture", None)
        # Draw rect if it has colors
        if color:
            rect = pygame.Rect(pos, size)
            pygame.draw.rect(window, color, rect)
            self.rect = rect
        # Add textures
        if texture:
            rect = pygame.Rect(pos, size)
            pygame.draw.rect(window, (0,0,0), rect)
            self.rect = rect
            image = pygame.transform.scale(pygame.image.load(texture), size)
            window.blit(image, pos)