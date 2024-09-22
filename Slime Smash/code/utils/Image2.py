from Setting import *

class Image2:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.initialImage = self.image.copy()
        self.initialRect = self.rect.copy()
        
        self.scalar = 1
        self.direction = 0
    
    def scaleImage(self, scalar):
        self.scalar = scalar
        self.__transform()
    
    def rotateImage(self, direction):
        self.direction = direction
        self.__transform()
    
    def setImage(self, image):
        self.initialImage = image
        self.__transform()
        
    def __transform(self):
        scaledImage = pygame.transform.scale(self.initialImage, (int(self.initialRect.width * self.scalar), int(self.initialRect.height * self.scalar)))
        self.image = pygame.transform.rotate(scaledImage, self.direction)
        self.rect = self.image.get_rect(center = self.initialRect.center)