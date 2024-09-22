from Setting import *
from utils.Image2 import *

class Background:
    def __init__(self):
        self.displaySurface = pygame.display.get_surface()
        self.damping = 70

        self.images = {
            "sky" : pygame.image.load("assets/background/sky.png").convert_alpha(),
            "hills" : pygame.image.load("assets/background/hills.png").convert_alpha(),
            "dojo" : pygame.image.load("assets/background/dojo.png").convert_alpha(),
            "trees" : pygame.image.load("assets/background/trees.png").convert_alpha(),
            "ground" : pygame.image.load("assets/background/ground.png").convert_alpha(),
            "shine" : pygame.image.load("assets/background/shine.png").convert_alpha()
        }

        self.sky = Image2(self.images["sky"])

        self.shine = Image2(self.images["shine"])
        self.shine.scaleImage(SCALAR)
        self.shine.rect.midtop = SCREEN_CENTER

        self.ground = Image2(self.images["ground"])
        self.ground.scaleImage(SCALAR)
        self.ground.rect.midtop = (SCREEN_WIDTH / 2, GROUND_Y)

        self.hills = Image2(self.images["hills"])
        self.hills.scaleImage(SCALAR)
        self.hills.rect.midtop = (SCREEN_WIDTH / 2, GROUND_Y - self.hills.rect.height + self.damping)
        
        self.dojo = Image2(self.images["dojo"])
        self.dojo.scaleImage(SCALAR)
        self.dojo.rect.midtop = (SCREEN_WIDTH / 2, GROUND_Y - self.dojo.rect.height + self.damping)

        self.trees = Image2(self.images["trees"])
        self.trees.scaleImage(SCALAR)
        self.trees.rect.midtop = (SCREEN_WIDTH / 2, GROUND_Y - self.trees.rect.height + self.damping)

        # motion
        self.angle = 0
    
    def update(self, dt, camera):
        self.shine.rotateImage(self.angle)
        self.shine.rect.center = SCREEN_CENTER
        self.angle -= 10 * dt

        self.hills.rect.top = GROUND_Y - self.hills.rect.height - camera.y / 9 + self.damping
        self.dojo.rect.top = GROUND_Y - self.dojo.rect.height - camera.y / 5 + self.damping
        self.trees.rect.top = GROUND_Y - self.trees.rect.height - camera.y / 3 + self.damping
        self.ground.rect.top = GROUND_Y - camera.y
    
    def draw(self):
        self.displaySurface.blit(self.sky.image, (0, 0))
        self.displaySurface.blit(self.shine.image, self.shine.rect.topleft)
        self.displaySurface.blit(self.hills.image, self.hills.rect.topleft)
        self.displaySurface.blit(self.dojo.image, self.dojo.rect.topleft)
        self.displaySurface.blit(self.trees.image, self.trees.rect.topleft)
        self.displaySurface.blit(self.ground.image, self.ground.rect.topleft)