import pygame, math, time

class Weapon:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.surface = pygame.Surface((16, 8))
        self.surface.fill((255, 255, 255))
        self.surface.set_colorkey((0, 0, 0))
        self.distance = 25
        self.projectileAngle = 0
        self.shooting = False
        self.lastShot = time.time()
        self.shootInterval = .05
        self.currentClip = 25
        self.reloading = False
        self.setReloadTime = time.time() 
        self.reloadTime = .25

    def draw(self, dest, playerCenter, cursorCenter, scroll):
        angle = self.findDrawAngle(playerCenter, cursorCenter, scroll)
        rotatedSurf = pygame.transform.rotate(self.surface, angle)
        dest.blit(rotatedSurf, (self.x - rotatedSurf.get_width() / 2 - scroll[0], self.y - rotatedSurf.get_height() / 2 - scroll[1]))

    def findDrawAngle(self, playerCenter, cursorCenter, scroll):
        dx = (playerCenter[0] - scroll[0]) - cursorCenter[0]
        dy = (playerCenter[1] - scroll[1]) - cursorCenter[1]
        angle = -math.degrees(math.atan(dy / (dx + 1)))
        return angle

    def findPositionAngle(self, playerCenter, cursorCenter, scroll):
        dx = (playerCenter[0] - scroll[0]) - cursorCenter[0]
        dy = (playerCenter[1] - scroll[1]) - cursorCenter[1]
        angle = -math.atan2(dy, dx)
        return angle

    def reposition(self, playerCenter, cursorCenter, scroll):
        angle = self.findPositionAngle(playerCenter, cursorCenter, scroll)
        self.projectileAngle = angle
        x = math.cos(angle) * self.distance
        y = math.sin(angle) * self.distance
        self.x = playerCenter[0] - x
        self.y = playerCenter[1] + y

    def update(self, dest, scroll, player, cursorCenter, projectileManager):
        self.reposition(player.rect.center, cursorCenter, scroll)
        self.draw(dest, player.rect.center, cursorCenter, scroll)
        if self.shooting:
            self.shoot(projectileManager, player.projectileRadius, player.projectileSpeed, player.projectileDamage, player.projectileHits)
        self.reloadClip()

    def reloadClip(self):
        if self.reloading and time.time() - self.setReloadTime >= self.reloadTime:
            self.currentClip = 25
            self.reloading = False

    def shoot(self, projectileManager, radius, speed, damage, hits):
        if self.currentClip > 0 and not self.reloading and time.time() - self.lastShot >= self.shootInterval:
            self.lastShot = time.time()
            projectileManager.add(self.x, self.y, 'player', self.projectileAngle, radius, speed, damage, hits)
            self.currentClip -= 1
        elif self.currentClip <= 0 and not self.reloading:
            self.setReloadTime = time.time()
            self.reloading = True


