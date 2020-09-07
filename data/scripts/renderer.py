import pygame

class Renderer:
    def __init__(self):
        pass
    
    def render(self, dest, scroll, tileScroll, objects, projectiles):
        objects.sort(key=lambda x: x.rect.bottom)
        [obj.draw(dest, scroll) for obj in objects]
        projectiles.sort(key=lambda x:x.rect.bottom)
        [projectile.draw(dest, scroll) for projectile in projectiles]