import pygame

class Transition:
    class WhiteFlash:
        def __init__(self):
            self.image = pygame.image.load("assets/effect/whiteFlash.png").convert_alpha()
            self.transparency = 255
        
        def reflash(self, flashPower):
            self.transparency = max(0, min(255, flashPower))
        
        def update(self, dt):
            self.transparency += (0 - self.transparency) * dt * 5
        
        def draw(self, displaySurface):
            self.image.set_alpha(self.transparency)
            displaySurface.blit(self.image, (0, 0))