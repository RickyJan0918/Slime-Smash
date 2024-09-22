from Setting import *
from utils.Image2 import *
from menus.Button import *
from Counter import *
import math

class GameOverMenu:
    def __init__(self, scores, highscore):
        self.counter = Counter(scores, pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20), 1.4)
        self.highscoreCounter = Counter(highscore, pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 110), 0.7)
        self.buttonGroup = pygame.sprite.Group()
        self.images = {
            "playButton" : pygame.image.load("assets/ui/playButton.png").convert_alpha(),
            "blackScreen" : pygame.image.load("assets/ui/blackScreen.png").convert_alpha(),
        }

        self.blackScreen = Image2(self.images["blackScreen"])
        self.blackScreenImage = self.blackScreen.image
        self.transparency = 0

        self.scalar = 2
        self.imageWidth = 21 * self.scalar
        self.position = pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        self.gap = 3

        self.gameOverLetters = []

        for i in range(8):
            letterImage = Image2(pygame.image.load(f"assets/ui/gameover{i}.png").convert_alpha())
            letterImage.scaleImage(self.scalar)
            positionX = self.position.x - self.imageWidth + ((i + 0.5) - 8 / 2) * (self.imageWidth + self.gap) * 2
            position = pygame.math.Vector2(positionX , self.position.y)
            self.gameOverLetters.append(GameOverLetter(letterImage.image, position, i))
        
        self.playButton = Image2(self.images["playButton"])
        self.playButton.scaleImage(SCALAR)

        self.playButton = Button(self.buttonGroup, self.playButton, (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 5 / 6), "playButton")

        self.running = False

        self.gongSound = pygame.mixer.Sound("audio/effect/gong.wav")
    
    def update(self, dt, scores, highscore):
        if not self.running: return
        self.transparency += (200 - self.transparency) * 10 * dt

        for letter in self.gameOverLetters:
            letter.update(dt)
        
        if self.playButton.onclick:
            self.gongSound.play()
            self.running = False
        
        self.counter.update(scores)
        self.highscoreCounter.update(highscore)
    
    def draw(self, displaySurface):
        self.blackScreenImage.set_alpha(self.transparency)
        displaySurface.blit(self.blackScreenImage, (0, 0))
        self.counter.draw(displaySurface)
        self.highscoreCounter.draw(displaySurface)

        for letter in self.gameOverLetters:
            letter.draw(displaySurface)

class GameOverLetter:
    def __init__(self, image, position, moveFrame):
        self.image = image
        self.position = position
        self.moveFrame = moveFrame
    
    def update(self, dt):
        self.position.y = 5 * math.sin(self.moveFrame) + SCREEN_HEIGHT / 4
        self.moveFrame += 10 * dt
    
    def draw(self, displaySurface):
        displaySurface.blit(self.image, self.position)