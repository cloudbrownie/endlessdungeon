import pygame, sys, os, ctypes, time, math

from data.scripts.cursor import Cursor
from data.scripts.gui_elems import TextButton
from data.scripts.font import Font
from data.scripts.mapmanager import MapManager
from data.scripts.player import Player
from data.scripts.weapon import Weapon
from data.scripts.projectiles import Projectile
from data.scripts.enemymanager import EnemyManager

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
        self.xResolution = 960
        self.yResolution = 540
        # ratio between screen dimensions and resolution
        self.xRatio = self.screenWidth / self.xResolution
        self.yRatio = self.screenHeight / self.yResolution
        # initialize screen and display
        self.screen = pygame.display.set_mode(size=(self.screenWidth, self.screenHeight), flags=pygame.NOFRAME)
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
        scroll[0] += (playerCenter[0] - scroll[0] - surf.get_width() / 2) / 10
        scroll[1] += (playerCenter[1] - scroll[1] - surf.get_height() / 2) / 10
        return scroll, (int(scroll[0]), int(scroll[1]))

    def MainMenu(self):
        # initial setup
        backgroundColor = 10, 15, 15
        buttonScale = 3
        buttons = [
            TextButton(self.xResolution * .1, self.yResolution * .7, 'Play', self.font, scale=buttonScale),
            TextButton(self.xResolution * .1, self.yResolution * .8, 'Settings', self.font, scale=buttonScale),
            TextButton(self.xResolution * .1, self.yResolution * .9, 'Exit', self.font, scale=buttonScale)
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
        mapManager = MapManager()
        enemyManager = EnemyManager()
        projectiles = []
        shooting = False
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
                        shooting = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.controls['shoot'] == 'mouse' and event.button == 1:
                        shooting = False

            # update game objects
            self.display.fill(backgroundColor)

            mapManager.updateMap(self.display, scroll=tileScroll)
            
            enemyManager.updateEnemies(self.display, scroll, player.rect.center, dt, mapManager.walls)
            
            player.update(self.display, scroll, dt, mapManager.walls)
            
            weapon.update(self.display, scroll, player.rect.center, self.cursor.center())
            
            if shooting and time.time() - weapon.lastShot >= weapon.shootInterval:
                projectiles.append(Projectile(weapon.x, weapon.y, 'player', weapon.projectileAngle))
                weapon.lastShot = time.time()
            
            projectileColliables = mapManager.walls.copy()
            projectileColliables.extend(enemyManager.enemies.copy())
            
            [projectile.update(self.display, scroll, dt, projectileColliables) for projectile in projectiles]
            [projectiles.remove(projectile) for projectile in projectiles if not projectile.alive]
            
            self.cursor.mouseUpdate(self.display)

            # update the screen
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(self.framerate)

    def Settings(self):
        print('Settings')

    def Exit(self):
        pygame.quit()
        sys.exit()

Game()