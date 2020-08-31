import pygame, math

def roundToWhole(val):
    return int(math.ceil(abs(val)) * (val / abs(val)))

class Player:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.surface = pygame.Surface((32, 32))
        self.surface.fill((255, 255, 255))
        self.vels = [0, 0]
        self.speed = 5
        self.movements = {'left':False, 'right':False, 'up':False, 'down':False}

    def draw(self, dest, scroll):
        dest.blit(self.surface, (self.rect.x - scroll[0], self.rect.y - scroll[1]))

    def move(self, dt):
        self.vels = [0, 0]

        if self.movements['left']:
            self.vels[0] -=  self.speed * dt
        if self.movements['right']:
            self.vels[0] += self.speed * dt
        if self.movements['up']:
            self.vels[1] -= self.speed * dt
        if self.movements['down']:
            self.vels[1] += self.speed * dt

        if self.vels[0] != 0:
            self.vels[0] = roundToWhole(self.vels[0])
        if self.vels[1] != 0:
            self.vels[1] = roundToWhole(self.vels[1])

    def collideTest(self, collidables):
        return [collidable for collidable in collidables if self.rect.colliderect(collidable)]

    def updateRect(self, tiles):
        self.rect.x += self.vels[0]
        hitList = self.collideTest(tiles)
        for tile in hitList:
            if self.vels[0] > 0:
                self.rect.right = tile.rect.left
            else:
                self.rect.left = tile.rect.right

        self.rect.y += self.vels[1]
        hitList = self.collideTest(tiles)
        for tile in hitList:
            if self.vels[1] > 0:
                self.rect.bottom = tile.rect.top
            else:
                self.rect.top = tile.rect.bottom

    def update(self, dest, scroll, dt, tiles):
        self.move(dt)
        self.updateRect(tiles)
        self.draw(dest, scroll)


