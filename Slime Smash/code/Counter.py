from Setting import *
from utils.Image2 import *

class Counter:
    def __init__(self, number, position, scalar):
        self.displaySurface = pygame.display.get_surface()
        self.number = str(number)
        self.images = { str(key) : pygame.image.load(f"assets/number/{key}.png").convert_alpha() for key in range(10) }
        self.position = position
        self.scalar = scalar
        self.imageWidth = 30 * self.scalar
        self.gap = 5 * self.scalar
    
    def update(self, number):
        self.number = str(number)
    
    def draw(self, displaySurface):
        i = 1
        for digit in self.number:
            digitImage = Image2(self.images[digit])
            digitImage.scaleImage(self.scalar)
            positionX = self.position.x - self.imageWidth + ((i - 0.5) - len(self.number) / 2) * (self.imageWidth + self.gap) * 2
            Number(digitImage.image, (positionX , self.position.y), displaySurface)
            i += 1

class Number:
    def __init__(self, image, position, displaySurface):
        self.image = image
        displaySurface.blit(self.image, position)
