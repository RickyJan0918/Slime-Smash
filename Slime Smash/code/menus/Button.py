from Setting import *

class Button(pygame.sprite.Sprite):
    def __init__(self, group, button, position, id):
        super().__init__(group)
        self.button = button
        self.image = button.image
        self.rect = button.rect
        self.position = position
        self.id = id
        self.onclick = False

        self.sizeScalar = SCALAR
        self.sizeScalarSpeed = 0

        self.detectMouseSound = pygame.mixer.Sound("audio/effect/detectMouse.wav")
        self.detectFrame = 1
    
    def jellyEffect(self, size, dt):
        self.sizeScalarSpeed = self.sizeScalarSpeed * 0.8 + (size - self.sizeScalar) * 10
        self.sizeScalar += self.sizeScalarSpeed * dt
        self.button.scaleImage(self.sizeScalar)
    
    def buttonOnClick(self, dt):
        mousePosition = pygame.mouse.get_pos()
        self.onclick = False
        if self.rect.collidepoint(mousePosition):
            if self.detectFrame == 0:
                self.detectMouseSound.play()
            self.jellyEffect(2.1, dt)
            if pygame.mouse.get_pressed()[0]:
                self.onclick = True
                self.jellyEffect(1.8, dt)
            self.detectFrame += 1
        else:
            self.jellyEffect(2, dt)
            self.detectFrame = 0
    
    def updateSprite(self):
        self.image = self.button.image
        self.rect = self.button.rect
        self.rect.center = self.position
    
    def update(self, dt):
        self.buttonOnClick(dt)
        self.updateSprite()