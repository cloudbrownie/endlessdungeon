import pygame, math, time

class Weapon:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.surface = pygame.Surface((32, 16))
        self.surface.fill((255, 255, 255))
        self.surface.set_colorkey((0, 0, 0))
        self.distance = 50
        self.projectileAngle = 0
        self.lastShot = time.time()
        self.shootInterval = .1

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

    def update(self, dest, scroll, playerCenter, cursorCenter):
        self.reposition(playerCenter, cursorCenter, scroll)
        self.draw(dest, playerCenter, cursorCenter, scroll)