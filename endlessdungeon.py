import pygame, sys, os, ctypes, time, math

from data.scripts.cursor import Cursor
from data.scripts.gui_elems import TextButton
from data.scripts.font import Font
from data.scripts.mapmanager import MapManager
from data.scripts.player import Player
from data.scripts.weapon import Weapon
from data.scripts.projectiles import Projectile
from data.scripts.projectilemanager import ProjectileManager
from data.scripts.enemymanager import EnemyManager
from data.scripts.portalmanager import PortalManager
from data.scripts.renderer import Renderer
from data.scripts.wavemanager import WaveManager

def deltaTime(prevTime):
    return time.time() - prevTime, time.time()

class Game:
    def __init__(self):
        # initializing sdl window settings
        user32 = ctypes.windll.user32
        os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
        pygame.init()
        # screen dimensions and resolution
        self.screenWidth = user32.GetSystemMetrics(0)
        self.screenHeight = user32.GetSystemMetrics(1)
        self.xResolution = 480
        self.yResolution = 270
        # ratio between screen dimensions and resolution
        self.xRatio = self.screenWidth / self.xResolution
        self.yRatio = self.screenHeight / self.yResolution
        # initialize screen and display
        self.screen = pygame.display.set_mode(size=(self.screenWidth, self.screenHeight), flags=pygame.NOFRAME | pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.display = pygame.Surface((self.xResolution, self.yResolution))
        # framerate
        self.clock = pygame.time.Clock()
        self.framerate = 60
        # custom cursor setup
        pygame.mouse.set_visible(False)
        self.cursor = Cursor('data/visuals/cursor.png', self.xRatio, self.yRatio)
        # custom font setup
        self.font = Font('data/visuals/font.png')
        # configurable controls
        self.controls = {'left':pygame.K_a, 'right':pygame.K_d, 'up':pygame.K_w, 'down':pygame.K_s, 'shoot':'mouse'}
        # start the main menu
        self.MainMenu()

    def updateScroll(self, scroll, playerCenter, surf):
        scroll[0] += (playerCenter[0] - scroll[0] - surf.get_width() / 2) / 2
        scroll[1] += (playerCenter[1] - scroll[1] - surf.get_height() / 2) / 2
        return scroll, (int(scroll[0]), int(scroll[1]))

    def MainMenu(self):
        # initial setup
        backgroundColor = 10, 15, 15
        buttonScale = 2
        buttons = [
            TextButton(self.xResolution * .15, self.yResolution * .7, 'Play', self.font, scale=buttonScale),
            TextButton(self.xResolution * .15, self.yResolution * .8, 'Settings', self.font, scale=buttonScale),
            TextButton(self.xResolution * .15, self.yResolution * .9, 'Exit', self.font, scale=buttonScale)
        ]
        options = {'Play':self.Play, 'Settings':self.Settings, 'Exit':self.Exit}
        selectedOption = None
        prevTime = time.time() + .001 
        while not selectedOption:

            dt, prevTime = deltaTime(prevTime)
            mx, my = pygame.mouse.get_pos()
            mousepos = mx / self.xRatio, my / self.yRatio

            # handle game events
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if [button for button in buttons if button.mouseCollide(mousepos)]:
                        selectedOption = options[[button.text for button in buttons if button.mouseCollide(mousepos)][0]]

            # update game objects
            self.display.fill(backgroundColor)
            [button.update(mousepos, self.display) for button in buttons]
            self.cursor.mouseUpdate(self.display)

            # update the screen 
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(self.framerate)
        
        selectedOption()

    def Play(self):
        print('Play')

        backgroundColor = 10, 15, 15
        player = Player()
        weapon = Weapon()
        portalManager = PortalManager()
        mapManager = MapManager(portalManager)
        enemyManager = EnemyManager()
        projectileManager = ProjectileManager()
        enemyManager.spawnEnemies(portalManager.portals)
        renderer = Renderer()
        waveManager = WaveManager()
        cameraRect = pygame.Rect(0, 0, self.xResolution, self.yResolution)
        self.font.recolor((255, 255, 255))
        scroll = [0, 0]
        prevTime = time.time() + .001
        running = True
        while running:

            dt, prevTime = deltaTime(prevTime)
            dt *= self.framerate

            scroll, tileScroll = self.updateScroll(scroll, player.rect.center, self.display)

            # handle game events
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.MainMenu()
                    elif event.key == self.controls['left']:
                        player.movements['left'] = True
                    elif event.key == self.controls['right']:
                        player.movements['right'] = True
                    elif event.key == self.controls['up']:
                        player.movements['up'] = True
                    elif event.key == self.controls['down']:
                        player.movements['down'] = True
                elif event.type == pygame.KEYUP:
                    if event.key == self.controls['left']:
                        player.movements['left'] = False
                    elif event.key == self.controls['right']:
                        player.movements['right'] = False
                    elif event.key == self.controls['up']:
                        player.movements['up'] = False
                    elif event.key == self.controls['down']:
                        player.movements['down'] = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.controls['shoot'] == 'mouse' and event.button == 1:
                        weapon.shooting = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.controls['shoot'] == 'mouse' and event.button == 1:
                        weapon.shooting = False

            # update game objects
            self.display.fill(backgroundColor)

            walls = mapManager.walls.copy()
            portals = portalManager.portals.copy()
            projectiles = projectileManager.projectiles.copy()
            enemies = enemyManager.enemies.copy()

            if enemyManager.getCount() == 0:
                waveManager.spawn(enemyManager, portals)

            enemyManager.updateEnemies(self.display, scroll, player.rect.center, dt, walls, projectileManager)
            
            portalManager.update()

            playerCollidables = walls
            playerCollidables.extend(portals)
            player.update(dt, playerCollidables)
            
            projectileCollidables = walls
            projectileCollidables.extend(enemies)
            projectileCollidables.append(player)
            projectileManager.update(dt, projectileCollidables)

            weapon.update(self.display, scroll, player, self.cursor.center(), projectileManager)

            entities = enemies
            entities.extend(walls)
            entities.extend(portals)
            entities.append(player)
            cameraRect.x = 0 + scroll[0]
            cameraRect.y = 0 + scroll[1]
            visibleEntities = [entity for entity in entities if entity.rect.colliderect(cameraRect)]

            renderer.render(self.display, scroll, tileScroll, visibleEntities, projectiles)

            self.cursor.mouseUpdate(self.display)

            self.font.render(self.display, f'{player.health}', (10, 10), scale=1)
            self.font.render(self.display, f'{weapon.currentClip}', (10, 20), scale=1)
            self.font.render(self.display, f'{enemyManager.getCount()}', (10, 30), scale=1)

            # update the screen
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            visibleRects = [entity.rect for entity in visibleEntities]
            pygame.display.update()
            self.clock.tick(self.framerate)

    def Settings(self):
        print('Settings')

    def Exit(self):
        pygame.quit()
        sys.exit()

Game()