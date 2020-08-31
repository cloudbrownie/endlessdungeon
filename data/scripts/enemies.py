import pygame, time, math

def roundToWhole(val):
    return int(math.ceil(abs(val)) * (val / abs(val)))

class Enemy:
    def __init__(self, x, y):
        self.tag = 'enemy'
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.rect.center = x, y
        self.surface = pygame.Surface(self.rect.size)
        self.surface.fill((100, 0, 0))
        self.health = 10
        self.speed = 3
        self.vels = [0, 0]

    def damage(self, val):
        self.health -= val

    def collideTest(self, tiles):
        return [tile for tile in tiles if self.rect.colliderect(tile.rect)]

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

    def draw(self, dest, scroll):
        dest.blit(self.surface, (self.rect.x - scroll[0], self.rect.y - scroll[1]))

    def update(self, dest, scroll):
        self.draw(dest, scroll)

class Ranged(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 250
        self.shootInterval = .25
        self.lastShot = time.time()
        self.inRange = False

    def attack(self):
        pass

    def move(self, playerCenter, dt):
        self.vels = [0, 0]
        dx = playerCenter[0] - self.rect.centerx
        dy = playerCenter[1] - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance > self.range:
            self.inRange = False
            dx /= distance
            dy /= distance
            self.vels[0] += self.speed * dx * dt
            self.vels[1] += self.speed * dy * dt

        else:
            self.inRange = True

    def update(self, dest, playerCenter, scroll, dt, tiles):
        self.move(playerCenter, dt)
        self.updateRect(tiles)
        self.draw(dest, scroll)




