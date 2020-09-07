import pygame, math, time

from data.scripts.projectiles import Projectile

class ProjectileManager:
    def __init__(self):
        self.projectiles = []
        self.length = len(self.projectiles)

    def update(self, dt, collidables):
        [projectile.update(dt, collidables) for projectile in self.projectiles]
        [self.projectiles.remove(projectile) for projectile in self.projectiles if not projectile.alive]
        self.length = len(self.projectiles)

    def add(self, x, y, tag, angle, radius, speed, damage, hits):
        if self.length < 100:
            self.projectiles.append(Projectile(x, y, tag, angle, radius, speed, damage, hits))