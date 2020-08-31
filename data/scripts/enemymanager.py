import pygame, time, math, random

from data.scripts.enemies import *

class EnemyManager:
    def __init__(self):
        self.credits = 100
        self.enemies = [Ranged(500, 600)]

    def createEnemies(self):
        for i in range(random.randint(1, 2)):
            self.enemies.append(Ranged(500, 600))

    def updateEnemies(self, dest, scroll, playerCenter, dt, tiles):
        [enemy.update(dest, playerCenter, scroll, dt, tiles) for enemy in self.enemies]
        [self.enemies.remove(enemy) for enemy in self.enemies if enemy.health <= 0]
