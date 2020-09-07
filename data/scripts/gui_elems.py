import pygame

class TextButton:
    def __init__(self, centerx, centery, text, font, scale=1, activeColor=(255, 255, 255), inactiveColor=(100, 100, 100)):
        self.font = font
        self.text = text
        self.center = centerx, centery
        self.scale = scale
        self.active = False
        self.activeSurf, self.activeRect = self.render(self.scale * 1.5, activeColor)
        self.inactiveSurf, self.inactiveRect = self.render(self.scale, inactiveColor)

    def render(self, scale, color):
        surf = pygame.Surface((self.font.size(self.text, scale)))
        surf.set_colorkey((0, 0, 0))
        self.font.recolor(color)
        self.font.render(surf, self.text, (0,0), scale)
        width = surf.get_width()
        height = surf.get_height()
        rect = pygame.Rect(0, 0, width, height)
        rect.center = self.center
        return surf, rect

    def getActive(self):
        return self.active
        
    def update(self, mousepos, dest):
        if self.mouseCollide(mousepos):
            dest.blit(self.activeSurf, self.activeRect)
            self.active = True
        else:
            dest.blit(self.inactiveSurf, self.inactiveRect)
            self.active = False

    def mouseCollide(self, mousepos):
        return self.inactiveRect.collidepoint(mousepos)
