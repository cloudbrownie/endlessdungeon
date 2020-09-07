import pygame, time, math, random

from data.scripts.enemies import *

class EnemyManager:
    def __init__(self):
        self.credits = 100
        self.enemyTypes = [SkeletonArcher]
        self.enemyCosts = {SkeletonArcher:10}
        self.enemies = []

    def getCount(self):
        return len(self.enemies)

    def spawnEnemies(self, portals):
        canBuy = True
        lowestPriced = min(self.enemyCosts[enemy] for enemy in self.enemyTypes)
        while canBuy:
            selectedEnemy = random.choice(self.affordableList())
            self.credits -= self.enemyCosts[selectedEnemy]
            canBuy = self.credits >= lowestPriced
            x, y = random.choice([portal.rect.center for portal in portals])
            self.enemies.append(selectedEnemy(x, y))
        
    def affordableList(self):
        return [enemy for enemy in self.enemyTypes if self.enemyCosts[enemy] <= self.credits]

    def updateEnemies(self, dest, scroll, playerCenter, dt, tiles, projectileManager):
        [enemy.update(dest, playerCenter, scroll, dt, tiles, projectileManager) for enemy in self.enemies]
        [self.enemies.remove(enemy) for enemy in self.enemies if enemy.health <= 0]
        
