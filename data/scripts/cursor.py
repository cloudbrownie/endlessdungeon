import pygame

from data.scripts.textures import loadTextures

class Cursor:
    def __init__(self, imagepath, xRatio, yRatio):
        images = loadTextures(imagepath, scale=3)
        self.defaultSurf = images[0][0]
        self.activeSurf = images[1][0]
        self.xRatio = xRatio
        self.yRatio = yRatio

    def mouseUpdate(self, dest):
        # get the current mouse position
        mx, my = pygame.mouse.get_pos()
        mx /= self.xRatio
        my /= self.yRatio
        # blit the correct cursor image
        if pygame.mouse.get_pressed()[0]:
            dest.blit(self.activeSurf, (mx - self.activeSurf.get_width() / 2, my - self.activeSurf.get_height() / 2))
        else:
            dest.blit(self.defaultSurf, (mx - self.defaultSurf.get_width() / 2, my - self.defaultSurf.get_height() / 2))