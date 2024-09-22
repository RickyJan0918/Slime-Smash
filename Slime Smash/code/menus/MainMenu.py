from Setting import *
from utils.Image2 import *
from menus.Button import *
import math

class MainMenu:
    def __init__(self, group):
        self.images = {
            "playButton" : pygame.image.load("assets/ui/playButton.png").convert_alpha(),
            "title" : pygame.image.load("assets/ui/title.png").convert_alpha(),
            "keyboard0" : pygame.image.load("assets/ui/keyboardHint1.png").convert_alpha(),
            "keyboard1" : pygame.image.load("assets/ui/keyboardHint2.png").convert_alpha()
        }

        self.playButton = Image2(self.images["playButton"])
        self.playButton.scaleImage(SCALAR)

        self.title = Image2(self.images["title"])
        self.title.scaleImage(SCALAR)

        self.keyboard = Image2(self.images["keyboard1"])
        self.keyboard.scaleImage(SCALAR)
        self.keyboardAnimationFrame = 0

        self.titleButton = Button(group, self.title, (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2 / 6), "title")
        self.playButton = Button(group, self.playButton, (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 5 / 6), "playButton")

        self.gongSound = pygame.mixer.Sound("audio/effect/gong.wav")
        self.nothingSound = pygame.mixer.Sound("audio/effect/nothing.wav")
        self.titleButtonDetectFrame = 1
        self.titleRotateFrame = 0

        self.running = False
    
    def update(self, dt):
        if not self.running: return
        self.title.rotateImage(3 * math.sin(self.titleRotateFrame))

        if self.titleButton.onclick:
            if self.titleButtonDetectFrame == 0:
                self.nothingSound.play()
            self.titleButtonDetectFrame += 1
        else:
            self.titleButtonDetectFrame = 0

        if self.playButton.onclick:
            self.gongSound.play()
            self.running = False
        
        self.keyboard.setImage(self.images[f"keyboard{int(self.keyboardAnimationFrame % 2)}"])
        self.keyboard.image.set_alpha(100)
        self.keyboardAnimationFrame += dt
        self.titleRotateFrame += dt * 3
    
    def draw(self, displaySurface):
        displaySurface.blit(self.keyboard.image, (10, SCREEN_HEIGHT * 0.7))