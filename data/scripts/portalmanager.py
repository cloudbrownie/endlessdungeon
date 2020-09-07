import pygame

class Portal:
    def __init__(self, xcoord, ycoord, size):
        self.tag = 'wall'
        self.coords = xcoord, ycoord
        self.rect = pygame.Rect(xcoord * size, ycoord * size, size, size)

    def draw(self, dest, scroll):
        pygame.draw.rect(dest, (255, 0, 0), (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.w, self.rect.h), 1)

class PortalManager:
    def __init__(self):
        self.portals = []

    def addPortal(self, coords, size):
        self.portals.append(Portal(coords[0], coords[1], size))
    
    def update(self):
        pass