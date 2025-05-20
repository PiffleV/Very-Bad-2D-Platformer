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
        self.cache = kwargs.get("cache", None)
        self.pos = pos
        self.size = size
        self.image = None
        self.size_scaled = size
        # Scale everything
        if self.scale:
            pos = tuple(map(lambda a: a*self.scale, pos))
            size = tuple(map(lambda a: a*self.scale, size))
            if self.shift:
                x,y = pos
                x -= self.shift
                pos = x,y
            self.size_scaled = size
        # Draw rect if it has colors
        if self.color:
            rect = pygame.Rect(pos, size)
            pygame.draw.rect(window, self.color, rect)
            self.rect = rect
        # Add textures
        if self.texture:
            rect = pygame.Rect(pos, size)
            self.rect = rect
            if self.cache:
                if (self.texture, size) in self.cache:
                    image = self.cache[(self.texture, size)]
                else:
                    image = pygame.transform.scale(pygame.image.load(self.texture), size)
            else:
                image = pygame.transform.scale(self.texture, size)
            self.image = image
            window.blit(image, pos)