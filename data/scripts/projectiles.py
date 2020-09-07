import pygame, math

def roundToWhole(val):
    return int(math.ceil(abs(val)) * (val / abs(val)))

class Projectile:
    def __init__(self, x, y, tag, angle, radius=5, speed=7, damage=5, hits=1):
        self.alive = True
        self.x = x
        self.y = y
        self.tag = tag
        self.radius = radius
        self.speed = speed
        self.angle = angle
        self.hits = hits
        self.damage = damage
        self.rect = pygame.Rect(0, 0, self.radius, self.radius)
        self.rect.center = x, y
        self.xVelocity = -self.speed * math.cos(self.angle)
        self.yVelocity = self.speed * math.sin(self.angle) 
        self.slope = self.vels[1] / self.vels[0]

    def outline(self, radius):
        glowSurface = pygame.Surface((radius * 2, radius * 2))
        if self.tag == 'player':
            pygame.draw.circle(glowSurface, (0, 150, 0), (radius, radius), radius)
        else:
            pygame.draw.circle(glowSurface, (150, 0, 0), (radius, radius), radius)
        glowSurface.set_colorkey((0, 0, 0))
        return glowSurface

    def draw(self, dest, scroll):
        pygame.draw.circle(dest, (255, 255, 255), (self.rect.x - scroll[0], self.rect.y - scroll[1]), self.radius)
        glowRadius = self.radius * 1.75
        dest.blit(self.outline(glowRadius), (self.rect.x - glowRadius - scroll[0], self.rect.y - glowRadius - scroll[1]), special_flags=pygame.BLEND_RGB_ADD)

    def updateRect(self, dt, collidables):
        xVel = roundToWhole(self.xVelocity)
        yVel = roundToWhole(self.yVelocity)

        xVel *= dt
        yVel *= dt

        xMovement = xVel
        yMovement = yVel


    def collide(self, collidables):
        collided = False
        for collidable in collidables:
            if self.rect.colliderect(collidable.rect):
                if collidable.tag != self.tag and collidable.tag != 'wall' and self.hits > 0:
                    collidable.damage(self.damage)
                    self.hits -= 1
                    collided = True
                elif collidable.tag == 'wall':
                    self.hits -= 1
                    collided = True
        return collided

    def update(self, dt, collidables):
        self.updateRect(collidables, dt)
        if self.hits <= 0:
            self.alive = False