from Setting import *
from Background import *
from menus.MainMenu import *
from menus.GameOverMenu import *
from sprites.Player import *
from sprites.Slime import *
from effects.Transition import *
from Counter import *

class MenuManager:
    def __init__(self):
        self.displaySurface = pygame.display.get_surface()
        self.allSprites = pygame.sprite.Group()
        self.background = Background()
        self.camera = pygame.math.Vector2(0, 0)
        self.running = True
    
    def spawnEnemy(self, times):
        if self.enemySpawnTick % times == 0:
            self.enemies.append(Slime(self.allSprites, self.camera))
        self.enemySpawnTick += 1
    
    def removeEnemy(self, enemy):
        self.enemies.remove(enemy)
        enemy.kill()
    
    def deleteEnemy(self):
        for enemy in self.enemies:
            if enemy.position.x > SCREEN_WIDTH + enemy.hitbox.width or enemy.position.x < -enemy.hitbox.width:
                self.removeEnemy(enemy)

class MainMenuManager(MenuManager):
    def __init__(self):
        super().__init__()
        self.menuSprites = pygame.sprite.Group()
        self.menu = MainMenu(self.menuSprites)
        self.player = Player(self.allSprites, self.camera)
        self.menu.running = True

    def updateMenu(self, dt):
        self.menu.update(dt)
        self.background.update(dt, self.camera)
        self.menuSprites.update(dt)
        self.background.draw()
        self.allSprites.draw(self.displaySurface)
        self.menuSprites.draw(self.displaySurface)
        self.menu.draw(self.displaySurface)
    
    def update(self, dt):
        if not self.running: return

        if self.menu.running:
            self.updateMenu(dt)
        else:
            self.running = False

class InGameMenuManager(MenuManager):
    def __init__(self, highscore):
        super().__init__()
        self.scores = 0
        self.player = Player(self.allSprites, self.camera)
        self.grameOverMenu = GameOverMenu(self.scores, highscore)
        self.counter = Counter(self.scores, pygame.math.Vector2(SCREEN_WIDTH / 2, 80), 1.2)
        self.whiteFlash = Transition.WhiteFlash()
        self.enemies = []
        self.enemySpawnTick = 0
        self.deathFrame = 0
        self.showGrameOverMenu = False
        self.grameOverMenu.running = True

        self.slimeSquishSound = pygame.mixer.Sound("audio/effect/slimeSquish.wav")
        self.playDeathSound = pygame.mixer.Sound("audio/effect/playerDeath.wav")
        self.gameOverSound = pygame.mixer.Sound("audio/effect/cheer.mp3")
    
    def rectVsRect(self, rectA, rectB):
        return (
            rectA.position.x + rectA.hitbox.width / 2 > rectB.position.x - rectB.hitbox.width / 2 and
            rectA.position.x - rectA.hitbox.width / 2 < rectB.position.x + rectB.hitbox.width / 2 and
            rectA.position.y - rectA.hitbox.height / 2< rectB.position.y + rectB.hitbox.height / 2 and
            rectA.position.y + rectA.hitbox.height / 2 > rectB.position.y - rectB.hitbox.height / 2
        )
    
    def checkCollision(self):
        if not self.player.isAlive: return

        for enemy in self.enemies:
            if self.rectVsRect(self.player, enemy):
                if self.player.position.y < enemy.position.y:
                    self.slimeSquishSound.play()
                    enemy.setToDeath()
                    self.enemies.remove(enemy)
                    self.whiteFlash.reflash(20)
                    self.scores += 1
                    self.player.jumping = 1
                    self.player.velocity.y = -self.player.jumpPower
                else:
                    self.playDeathSound.play()
                    self.player.velocity.x = 0
                    self.player.velocity.y = -1000
                    self.whiteFlash.reflash(80)
                    self.player.setToDeath()

    def updateMenu(self, dt, highscore):
        self.spawnEnemy(50)
        self.deleteEnemy()
        self.checkCollision()
        self.setCamera()

        self.background.update(dt, self.camera)
        self.counter.update(self.scores)
        self.allSprites.update(dt)
        self.whiteFlash.update(dt)
        if self.showGrameOverMenu:
            self.grameOverMenu.update(dt, self.scores, highscore)
            self.grameOverMenu.buttonGroup.update(dt)

        self.background.draw()
        self.counter.draw(self.displaySurface)
        self.allSprites.draw(self.displaySurface)
        self.whiteFlash.draw(self.displaySurface)
        if self.showGrameOverMenu:
            self.grameOverMenu.draw(self.displaySurface)
            self.grameOverMenu.buttonGroup.draw(self.displaySurface)
    
    def setCamera(self):
        self.camera.y = (self.player.rect.bottom - GROUND_Y) / 4
        if self.camera.y > 0:
            self.camera.y = 0
    
    def update(self, dt, highscore):
        if not self.running: return
        if not self.player.isAlive:
            if self.deathFrame == 100:
                self.gameOverSound.play()
                self.showGrameOverMenu = True
            self.deathFrame += 1

        if self.grameOverMenu.running:
            self.updateMenu(dt, highscore)
        else:
            self.running = False