import pygame, sys, os, ctypes

class Game:
    def __init__(self):
        user32 = ctypes.windll.user32
        os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
        pygame.init()
        self.screenWidth = user32.GetSystemMetrics(0)
        self.screenHeight = user32.GetSystemMetrics(1)
        self.xResolution = 1920
        self.yResolution = 1080
        self.xRatio = self.screenWidth / self.xResolution
        self.yRatio = self.screenHeight / self.yResolution

Game()