import pygame, math

class Projectile:
    def __init__(self, x, y, tag, angle, modifiers=[]):
        self.alive = True
        self.x = x
        self.y = y
        self.tag = tag
        self.radius = 10
        self.speed = 10
        self.angle = angle
        self.hits = 1
        self.damage = 5
        self.rect = pygame.Rect(0, 0, self.radius, self.radius)
        self.rect.center = x, y

    def applyModifiers(self, modifiers):
        pass

    def outline(self, radius):
        glowSurface = pygame.Surface((radius * 2, radius * 2))
        if self.tag == 'player':
            pygame.draw.circle(glowSurface, (0, 100, 20), (radius, radius), radius)
        else:
            pygame.draw.circle(glowSurface, (100, 0, 0), (radius, radius), radius)
        glowSurface.set_colorkey((0, 0, 0))
        return glowSurface

    def draw(self, dest, scroll):
        pygame.draw.circle(dest, (255, 255, 255), (self.rect.x - scroll[0], self.rect.y - scroll[1]), self.radius)
        dest.blit(self.outline(self.radius * 2), (self.rect.x - self.radius * 2 - scroll[0], self.rect.y - self.radius * 2 - scroll[1]), special_flags=pygame.BLEND_RGB_ADD)

    def move(self, dt):
        self.rect.x -= self.speed * math.cos(self.angle) * dt
        self.rect.y += self.speed * math.sin(self.angle) * dt

    def collide(self, collidables):
        for collidable in collidables:
            if self.rect.colliderect(collidable.rect):
                self.hits -= 1
                if collidable.tag != 'wall':
                    collidable.damage(self.damage)

    def update(self, dest, scroll, dt, collidables):
        self.move(dt)
        self.collide(collidables)
        if self.hits <= 0:
            self.alive = False
        if self.alive:
            self.draw(dest, scroll)