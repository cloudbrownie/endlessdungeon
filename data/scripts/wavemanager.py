import pygame

class WaveManager:
    def __init__(self):
        self.wave = 0
        self.scale = 1

    def spawn(self, enemyManager, portals):
        enemyManager.credits = 100 * (self.scale / 2)
        enemyManager.spawnEnemies(portals)
        self.wave += 1
        self.scale += .5