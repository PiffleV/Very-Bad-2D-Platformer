# Library Import
import pygame
pygame.init()
# Get Rectangle
class drawRect:
    def __init__(self, window, pos: tuple, size: tuple, **kwargs):
        # Get color or texture if it exists, also get scale if it exists
        self.color = kwargs.get('color',None)
        self.texture = kwargs.get("texture", None)
        self.scale = kwargs.get("scale", None)
        self.shift = kwargs.get("shift", None)
        self.pos = pos
        self.size = size
        # Scale everything
        if self.scale:
            pos = tuple(map(lambda a: a*self.scale, pos))
            size = tuple(map(lambda a: a*self.scale, size))
            if self.shift:
                x,y = pos
                x -= self.shift
                pos = x,y
        # Draw rect if it has colors
        if self.color:
            rect = pygame.Rect(pos, size)
            pygame.draw.rect(window, self.color, rect)
            self.rect = rect
        # Add textures
        if self.texture:
            rect = pygame.Rect(pos, size)
            pygame.draw.rect(window, (0,0,0), rect)
            self.rect = rect
            image = pygame.transform.scale(self.texture, size)
            window.blit(image, pos)