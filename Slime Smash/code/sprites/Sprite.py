from Setting import *
from utils.Image2 import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, group, camera):
        super().__init__(group)
        self.displaySurface = pygame.display.get_surface()
        self.camera = camera
        self.isAlive = True
    
    def integrate(self, dt):
        self.velocity.y += GRAVITY * dt
        self.position += self.velocity * dt
        self.falling += 1
    
    def setToDeath(self):
        self.isAlive = False
    
    def collisionY(self):
        if self.position.y + self.hitbox.height / 2 > GROUND_Y:
            self.position.y = GROUND_Y - self.hitbox.height / 2
            self.velocity.y = 0
            self.falling = 0
    
    def setPositionWithCamera(self):
        self.hitbox.center = (self.position.x - self.camera.x, self.position.y - self.camera.y)
        self.rect.center = self.hitbox.center