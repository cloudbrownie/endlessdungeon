import pygame

from data.scripts.textures import loadTextures

class Cursor:
    def __init__(self, imagepath, xRatio, yRatio):
        images = loadTextures(imagepath, colorkey=(0, 0, 0), scale=3)
        self.defaultSurf = images[0][0]
        self.activeSurf = images[1][0]
        self.xRatio = xRatio
        self.yRatio = yRatio
        self.x = 0
        self.y = 0

    def mouseUpdate(self, dest):
        # get the current mouse position
        mx, my = pygame.mouse.get_pos()
        self.x = mx / self.xRatio
        self.y = my / self.yRatio
        # blit the correct cursor image
        if pygame.mouse.get_pressed()[0]:
            dest.blit(self.activeSurf, (self.x - self.activeSurf.get_width() / 2, self.y - self.activeSurf.get_height() / 2))
        else:
            dest.blit(self.defaultSurf, (self.x - self.defaultSurf.get_width() / 2, self.y - self.defaultSurf.get_height() / 2))

    def center(self):
        return self.x, self.y