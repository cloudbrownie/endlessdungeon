import pygame, random

from data.scripts.textures import loadTextures
from data.scripts.portalmanager import PortalManager, Portal

class Tile:
    def __init__(self, xcoord, ycoord, size):
        self.tag = 'wall'
        self.coords = xcoord, ycoord
        self.rect = pygame.Rect(xcoord * size, ycoord * size, size, size)

    def draw(self, dest, scroll):
        pygame.draw.rect(dest, (255, 255, 255), (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.w, self.rect.h), 1)

class MapManager:
    def __init__(self, portalManager):
        mapsrc = pygame.image.load('data/visuals/mapsrc.png')
        tiles = self.createTiles(mapsrc)
        self.size = 16
        self.walls = self.createWalls(tiles, portalManager)

    def createTiles(self, mapsrc):
        tiles = []
        for i in range(mapsrc.get_width()):
            tiles.append([])
            for j in range(mapsrc.get_height()):
                if mapsrc.get_at((i, j)) == (55, 148, 110, 255):
                    tiles[i].append(1)
                elif mapsrc.get_at((i, j)) == (229, 25, 138, 255):
                    tiles[i].append(2)
                else:
                    tiles[i].append(0)
        return tiles

    def createWalls(self, tiles, portalManager):
        walls = []
        for i in range(len(tiles)):
            for j in range(len(tiles[i])):
                if tiles[i][j] == 1:
                    walls.append(Tile(i, j, self.size))
                elif tiles[i][j] == 2:
                    portalManager.addPortal((i, j), self.size)
        return walls